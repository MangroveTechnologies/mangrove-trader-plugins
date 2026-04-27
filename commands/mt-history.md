---
name: mt-history
description: View trade history (own free, others x402 paid $0.01/3 trades)
---

# mt-history

View a trader's complete trade history. Your own history is free.

## Steps

1. Ask for the Twitter handle to look up, and optional trade limit (0 = all, max 1000).
2. **If looking up your own history**: Check `MT_AUTH_TOKEN` env var. If set, call `trader_get_trade_history` with `twitter_handle` AND `auth_token`. No payment needed -- data returns directly with `"access": "free"`.
3. **If MCP tool is not available for own history**, fall back to REST: `POST https://api.mangrovetraders.com/api/v1/trader/trade_history` with `{"twitter_handle": "<handle>", "auth_token": "<token>"}`
4. **If looking up someone else's history**: call `trader_get_trade_history` WITHOUT `payment` parameter first. Server returns PAYMENT_REQUIRED with total trades and computed price.
5. Present: "X trades available, cost is $Y USDC. Proceed?"
6. **If payment capability available**: sign x402 payment, call again WITH `payment`, present trade list (action, symbol, asset class, quantity, price, timestamp)
7. **If no payment capability**: tell the user this tool requires x402 payment signing with an EVM wallet holding USDC on Base. Ask them to provide their EVM wallet private key. Once provided, persist it for future sessions using the platform-appropriate method, then set it in the current session and retry from step 4:
   - **macOS**: append `export MT_WALLET_PRIVATE_KEY=<key>` to `~/.zshenv`
   - **Linux**: append `export MT_WALLET_PRIVATE_KEY=<key>` to `~/.bashrc` (or `~/.profile` for login shells)
   - **Windows (PowerShell)**: run `[System.Environment]::SetEnvironmentVariable('MT_WALLET_PRIVATE_KEY', '<key>', 'User')` to persist at user level; also set in current session with `$env:MT_WALLET_PRIVATE_KEY='<key>'`
   - If the user does not have a wallet, suggest `/mt-last` (free, shows most recent trade only) or the REST API with an API key

## Pricing

- **Your own trades**: Free (always, with auth_token)
- **Others' trades**: $0.01 per 3 trades (rounded up)
- Examples: 3 trades = $0.01, 10 trades = $0.04, 100 trades = $0.34, 1000 trades = $3.34
