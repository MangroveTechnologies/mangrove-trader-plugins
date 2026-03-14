---
name: search-trader
description: Use when the user wants to look up another trader's profile or stats
---

# Search Trader ($0.02 USDC on Base)

## Steps

1. Get Twitter handle to search
2. Call `trader_search_trader` WITHOUT payment
3. Server returns PAYMENT_REQUIRED ($0.02 USDC)
4. Ask user to confirm
5. Call WITH payment
6. Present full profile: score, rank, recent trades, breakdown
