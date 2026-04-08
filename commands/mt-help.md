---
name: mt-help
description: Show all MangroveTrader plugin commands
---

# mt-help

Display all available MangroveTrader commands.

## Output

Present this to the user:

```
MangroveTrader — mangrovetraders.com

Getting started:
  1. /mt-set-handle   Verify your X identity (required for all commands)
  2. /mt-track        Compose and tweet a trade to @MangroveTrader
  3. /mt-stats        Check your score and rank

Commands:
  /mt-set-handle                       Verify your X identity
  /mt-track                            Compose a trade tweet
  /mt-stats                            Score, rank, open positions
  /mt-report [timeframe]               Performance breakdown
  /mt-last [handle]                    Most recent trade
  /mt-history [handle] [limit]         Trade history (own free, others $0.01/3)
  /mt-leaderboard [timeframe] [limit]  Rankings ($0.25+)
  /mt-search <query>                   Find a trader ($0.02)
  /mt-cancel                           Cancel last trade (5-min window)
  /mt-watch <target>                   Watch a trader
  /mt-unwatch <target>                 Unwatch a trader
  /mt-status                           Server health
  /mt-help                             This help message

All commands require MT_AUTH_TOKEN to be set. Run /mt-set-handle to verify your identity.
Trades submitted by tweeting @MangroveTrader. Paid tools use x402 (USDC on Base).
```
