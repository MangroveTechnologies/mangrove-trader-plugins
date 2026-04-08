---
name: mt-search
description: Search for a trader by handle or name (x402 paid, $0.02 USDC on Base)
---

# mt-search

Search for a trader on MangroveTrader.

This is an x402 paid tool ($0.02 USDC on Base).

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If not set, call `trader_login` to get a verification URL and stop.
2. Ask for the search query — Twitter handle or display name.
3. Call `trader_search_trader` MCP tool WITHOUT the `payment` parameter, with `query`.
4. Server returns PAYMENT_REQUIRED ($0.02 USDC).
5. Present the price and ask to confirm.
6. **If payment capability available**: sign x402 payment, call again WITH `payment`, present results (handle, display name, score, rank, trade count, qualified status).
7. **If no payment capability**: suggest `/mt-stats <handle>` (free, if they know the exact handle).

## Parameters

- `query`: Search string — handle or display name (max 100 chars)
- `limit`: 1-50 results (default: 20)
- `payment`: signed x402 payment header (from step 6)
