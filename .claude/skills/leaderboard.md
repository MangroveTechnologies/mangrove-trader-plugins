---
name: leaderboard
description: Use when the user wants to see the trading leaderboard, top traders, or rankings
---

# Leaderboard ($0.25 USDC on Base)

## Steps

1. Call `trader_get_leaderboard` WITHOUT payment
2. Server returns PAYMENT_REQUIRED ($0.25 USDC)
3. Tell user the cost, ask to proceed
4. If confirmed, call WITH payment (x402 signature)
5. Present top traders with rank, score, return %

Params: timeframe (daily/weekly/monthly/all_time), limit (default 100)

If declined: their own rank is free via my-portfolio. Daily top 10 on Twitter @MangroveTrader.
