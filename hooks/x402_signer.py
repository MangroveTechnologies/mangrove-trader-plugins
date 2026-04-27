#!/usr/bin/env python3
"""x402 auto-pay hook for MangroveTrader MCP tools.

PostToolUse hook. When an x402-gated MCP tool returns PAYMENT_REQUIRED,
this script signs the payment and retries via the REST API, injecting
the real result as context so Claude doesn't need to re-invoke the tool.

Required:
  MT_WALLET_PRIVATE_KEY   EVM private key (hex, with or without 0x prefix)

Optional:
  MT_API_BASE_URL         API base URL (default: https://api.mangrovetraders.com)
  MT_MAX_PAYMENT_USD      Max USDC to auto-sign per request (default: 0.30)

Install dependencies:
  pip install "x402[evm]" eth-account httpx
"""

import asyncio
import json
import logging
import os
import sys

# Redirect all library logging to stderr so stdout stays clean for hook JSON output
logging.basicConfig(stream=sys.stderr)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


# Short tool names (after stripping MCP prefix) that require x402 payment
X402_TOOLS = frozenset({
    "trader_get_leaderboard",
    "trader_search_trader",
    "trader_get_trade_history",
})

REST_BASE = os.environ.get("MT_API_BASE_URL", "https://api.mangrovetraders.com")
MAX_PAYMENT_USD = float(os.environ.get("MT_MAX_PAYMENT_USD", "0.30"))

# Maps MCP tool name -> REST endpoint config
TOOL_CONFIG = {                                                                                                                               
    "trader_get_leaderboard": {                                                                                                               
        "path": "/api/x402/leaderboard",                                                                                                      
        "payment_header": "payment-signature",                                                                                                        
    },                                                                                                                                        
    "trader_search_trader": {                                                                                                                 
        "path": "/api/x402/search",                                                                                                           
        "payment_header": "payment-signature",                                                                                                        
    },                                                                                                                                        
    "trader_get_trade_history": {                                                                                                             
        "path": "/api/x402/trade_history",                                                                                                    
        "payment_header": "X-Payment",                                                                                                        
    },                                                                                                                                        
}   


# ---------------------------------------------------------------------------
# Signer (mirrors EthAccountSigner in e2e_payment_test.py)
# eth-account 0.13+ requires full_message dict format for sign_typed_data
# ---------------------------------------------------------------------------

class _EthAccountSigner:
    def __init__(self, private_key: str):
        from eth_account import Account
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        self.account = Account.from_key(private_key)
        self.address = self.account.address

    def sign_typed_data(self, domain, types, primary_type, message) -> bytes:
        domain_dict = {
            "name": domain.name,
            "version": domain.version,
            "chainId": domain.chain_id,
            "verifyingContract": domain.verifying_contract,
        }
        domain_dict = {k: v for k, v in domain_dict.items() if v is not None}
        if hasattr(domain, "salt") and domain.salt is not None:
            domain_dict["salt"] = domain.salt

        types_dict = {}
        for type_name, fields in types.items():
            types_dict[type_name] = [{"name": f.name, "type": f.type} for f in fields]

        full_message = {
            "types": types_dict,
            "primaryType": primary_type,
            "domain": domain_dict,
            "message": dict(message),
        }
        signed = self.account.sign_typed_data(full_message=full_message)
        return signed.signature


# ---------------------------------------------------------------------------
# REST body builder — maps MCP tool input to REST request body
# ---------------------------------------------------------------------------

def _build_rest_body(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "trader_get_leaderboard":
        body = {}
        if "timeframe" in tool_input:
            body["timeframe"] = tool_input["timeframe"]
        if "limit" in tool_input:
            body["limit"] = tool_input["limit"]
        return body

    if tool_name == "trader_search_trader":
        # MCP uses "query"; REST uses "twitter_handle"
        return {
            "twitter_handle": tool_input.get("query", ""),
            "limit": tool_input.get("limit", 20),
        }

    if tool_name == "trader_get_trade_history":
        body = {"twitter_handle": tool_input.get("twitter_handle", "")}
        if tool_input.get("limit"):
            body["limit"] = tool_input["limit"]
        return body

    return {}


# ---------------------------------------------------------------------------
# Price parsing
# ---------------------------------------------------------------------------

def _parse_price(price_str: str) -> float:
    """'$0.25' -> 0.25"""
    return float(str(price_str).lstrip("$"))


# ---------------------------------------------------------------------------
# Core async signing + REST call
# ---------------------------------------------------------------------------

async def _sign_and_call(
    payment_required_b64: str,
    tool_name: str,
    tool_input: dict,
    private_key: str,
) -> dict:
    from x402 import x402Client
    from x402.http.utils import decode_payment_required_header, encode_payment_signature_header
    from x402.mechanisms.evm.exact import register_exact_evm_client
    import httpx

    signer = _EthAccountSigner(private_key)
    client = x402Client()
    register_exact_evm_client(client, signer)

    payment_required = decode_payment_required_header(payment_required_b64)
    payload = await client.create_payment_payload(payment_required)
    signed_payment = encode_payment_signature_header(payload)

    cfg = TOOL_CONFIG[tool_name]
    body = _build_rest_body(tool_name, tool_input)
    headers = {
        "Content-Type": "application/json",
        cfg["payment_header"]: signed_payment,
    }

    async with httpx.AsyncClient(timeout=20.0) as http:
        resp = await http.post(f"{REST_BASE}{cfg['path']}", json=body, headers=headers)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Hook entrypoint
# ---------------------------------------------------------------------------

def main():
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)

    try:
        event = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    raw_tool_name = event.get("tool_name", "")
    # Strip MCP server prefix: "mcp__mangrove-trader__trader_get_leaderboard" -> "trader_get_leaderboard"
    tool_name = raw_tool_name.split("__")[-1]
    if tool_name not in X402_TOOLS:
        sys.exit(0)

    # Parse tool response (may be a JSON string or already a dict)
    tool_response = event.get("tool_response", "")
    if isinstance(tool_response, str):
        try:
            response_data = json.loads(tool_response)
        except (json.JSONDecodeError, ValueError):
            sys.exit(0)
    else:
        response_data = tool_response

    if not isinstance(response_data, dict):
        sys.exit(0)

    # Unwrap MCP envelope: {"result": "<json string>"} -> inner dict
    if "result" in response_data and "code" not in response_data:
        inner = response_data["result"]
        if isinstance(inner, str):
            try:
                response_data = json.loads(inner)
            except (json.JSONDecodeError, ValueError):
                sys.exit(0)
        elif isinstance(inner, dict):
            response_data = inner

    if response_data.get("code") != "PAYMENT_REQUIRED":
        sys.exit(0)

    # Validate price against cap before touching the wallet
    price_str = response_data.get("price", "$0.00")
    try:
        price = _parse_price(price_str)
    except (ValueError, TypeError):
        _output_context(f"[x402] Could not parse price '{price_str}'. Not signing.")
        sys.exit(0)

    if price > MAX_PAYMENT_USD:
        _output_context(
            f"[x402] Refused: server requested {price_str} USDC "
            f"which exceeds the auto-pay cap of ${MAX_PAYMENT_USD:.2f}. "
            f"Set MT_MAX_PAYMENT_USD to a higher value to allow this, "
            f"or pay manually."
        )
        sys.exit(0)

    private_key = os.environ.get("MT_WALLET_PRIVATE_KEY", "").strip()
    if not private_key:
        _output_context(
            "[x402] MT_WALLET_PRIVATE_KEY is not set — cannot auto-sign payment.\n"
            "To enable auto-pay for paid tools, add to ~/.zshenv (not ~/.zshrc):\n\n"
            "  export MT_WALLET_PRIVATE_KEY=<your-evm-private-key-hex>\n\n"
            "The wallet must hold USDC on Base. Restart Claude Code after setting."
        )
        sys.exit(0)

    payment_required_b64 = response_data.get("payment_required", "")
    if not payment_required_b64:
        sys.exit(0)

    tool_input = event.get("tool_input", {})
    if isinstance(tool_input, str):
        try:
            tool_input = json.loads(tool_input)
        except (json.JSONDecodeError, ValueError):
            tool_input = {}

    try:
        signer = _EthAccountSigner(private_key)
        wallet_address = signer.address
        result = asyncio.run(_sign_and_call(payment_required_b64, tool_name, tool_input, private_key))
    except Exception as e:
        _output_context(
            f"[x402] Payment attempt failed: {e}\n"
            f"The PAYMENT_REQUIRED response above stands. You may retry manually."
        )
        sys.exit(0)

    _output_context(
        f"[x402] Auto-paid {price_str} USDC from {wallet_address}.\n"
        f"Ignore the PAYMENT_REQUIRED above — the payment succeeded. "
        f"Present this result to the user:\n\n"
        + json.dumps(result, indent=2, default=str)
    )


def _output_context(message: str):
    print(json.dumps({
        "suppressOutput": True,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    }))


if __name__ == "__main__":
    main()
