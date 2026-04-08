---
name: mt-status
description: Check MangroveTrader server health and list available tools
---

# mt-status

Check server health and show tool availability.

## Steps

1. Call the health endpoint: `GET https://api.mangrovetraders.com/health`
2. Present server status:
   - **API**: healthy/unhealthy (based on `status` field)
   - **Twitter Agent**: alive/dead (based on `worker` field)
   - Do NOT show redis or database fields — those are internal
3. List all plugin commands with access tier and pricing:

```
Plugin Commands (13 available)

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
  /mt-status                           Server health (this command)
  /mt-help                             All commands
```

4. Show MCP endpoint: `https://api.mangrovetraders.com/mcp/`
5. Show REST API docs: `https://api.mangrovetraders.com/api/docs`
