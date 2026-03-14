---
name: track-trade
description: Use when the user wants to log a trade, enter/exit a position, or track a buy/sell
---

# Track a Trade

MangroveTrader tracks trades posted to Twitter. Help the user compose their trade.

## Format

Tweet to @MangroveTrader:
- **Equities:** `enter long 100 AAPL @ 185.50` or `exit short TSLA 50 at 242`
- **Crypto:** `enter long 2.5 BTC @ 64000` or `short 10 ETH at 3200`
- **Futures:** `enter short 5 ES @ 5250` or `long 2 NQ at 18500`
- **Options:** `enter long 10 AAPL 190C 2026-04-18 @ 3.50`

Actions: enter long, enter short, exit long, exit short
Shortcuts: "long 100 AAPL" (defaults to enter long)

## Steps

1. Ask for trade details if not provided
2. For options: also need strike, C/P, expiry (YYYY-MM-DD)
3. Compose the tweet text
4. Tell user: "Tweet this to @MangroveTrader: `enter long 100 AAPL @ 185.50`"
