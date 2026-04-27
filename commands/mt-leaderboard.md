---
name: mt-leaderboard
description: View the MangroveTrader leaderboard rankings (x402 paid, $0.25+ USDC on Base). Top 5 free on Twitter.
---

# mt-leaderboard

View the full MangroveTrader leaderboard.

This is an x402 paid tool. The agent or user must pay in USDC on Base to access the data.

**Tip:** The top 5 is always free by tweeting "leaderboard" to @MangroveTrader on Twitter.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If not set, call `trader_login` to get a verification URL and stop.
2. Ask for optional parameters:
   - **Timeframe**: daily, weekly, monthly, all_time, 30d, 7d (default: all_time)
   - **Limit**: 1-500 rows (default: 100)
3. Call `trader_get_leaderboard` MCP tool WITHOUT the `payment` parameter.
4. The server returns PAYMENT_REQUIRED with:
   - `price`: cost in USDC (e.g., "$0.25")
   - `payment_required`: base64-encoded x402 payment requirements
5. Present the price to the user and ask to confirm.
6. **If the user/agent has x402 payment capability** (EVM wallet with USDC on Base):
   - Sign the payment using the x402 protocol against the requirements
   - Call `trader_get_leaderboard` again WITH the signed `payment` parameter
   - Present the leaderboard: rank, handle, score, return %
7. **If no payment capability**: tell the user this tool requires x402 payment signing with an EVM wallet holding USDC on Base. Ask them to provide their EVM wallet private key. Once provided, persist it for future sessions using the platform-appropriate method, then set it in the current session and retry from step 3:
   - **macOS**: append `export MT_WALLET_PRIVATE_KEY=<key>` to `~/.zshenv`
   - **Linux**: append `export MT_WALLET_PRIVATE_KEY=<key>` to `~/.bashrc` (or `~/.profile` for login shells)
   - **Windows (PowerShell)**: run `[System.Environment]::SetEnvironmentVariable('MT_WALLET_PRIVATE_KEY', '<key>', 'User')` to persist at user level; also set in current session with `$env:MT_WALLET_PRIVATE_KEY='<key>'`
   - If the user does not have a wallet, suggest alternatives:
     - Own rank is always free via `/mt-stats`
     - Use the REST API at `https://api.mangrovetraders.com/api/x402/leaderboard` with an API key (X-API-Key header bypasses payment)
     - Daily top 10 posted on @MangroveTrader Twitter

## Pricing

- $0.25 for up to 100 rows
- +$0.01 per 4 additional rows beyond 100
- Max 500 rows
- Examples: 100 rows = $0.25, 200 rows = $0.50, 500 rows = $1.25
