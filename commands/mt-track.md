---
name: mt-track
description: Compose a trade tweet to submit to @MangroveTrader on Twitter
---

# mt-track

Help the user compose a trade tweet for @MangroveTrader.

Trades are submitted by tweeting to @MangroveTrader on Twitter. This command helps format the tweet correctly.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If not set, call `trader_login` to get a verification URL and stop.
2. Ask for trade details if not provided:
   - **Action**: enter long, enter short, exit long, exit short (shortcuts: long, short, bought, sold, grabbed, dumped, faded)
   - **Quantity**: number of units
   - **Symbol**: ticker (BTC, AAPL, ES, etc.)
   - **Price**: entry/exit price
3. For options, also ask:
   - **Strike**: strike price
   - **Type**: C (call) or P (put)
   - **Expiry**: YYYY-MM-DD format
4. Compose the tweet text in the correct format.
5. Tell the user: "Tweet this to @MangroveTrader on Twitter:"
6. Show the formatted trade text.

## Tweet Formats

| Asset Class | Format | Example |
|-------------|--------|---------|
| Equities | `enter long QTY SYMBOL @ PRICE` | `enter long 100 AAPL @ 185.50` |
| Crypto | `enter long QTY SYMBOL @ PRICE` | `enter long 2.5 BTC @ 64000` |
| Futures | `enter short QTY SYMBOL @ PRICE` | `enter short 5 ES @ 5250` |
| Options | `enter long QTY SYMBOL STRIKE[C/P] EXPIRY @ PRICE` | `enter long 10 AAPL 190C 2026-04-18 @ 3.50` |

## Shortcuts

`long 100 AAPL` defaults to `enter long`. Other shortcuts: `bought`, `sold`, `grabbed`, `dumped`, `faded`, `cover`.
