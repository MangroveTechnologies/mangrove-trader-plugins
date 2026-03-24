---
name: mt-status
description: Check MangroveTrader server health and list available tools
---

# mt-status

Check server health and show tool availability.

## Steps

1. Call the health endpoint: `GET https://api.mangrovetraders.com/health`
2. Present server status:
   - **Status**: healthy/unhealthy
   - **Redis**: connected/disconnected
   - **Database**: connected/disconnected
   - **Worker**: alive/dead (the Twitter polling agent)
3. List all MCP tools with access tier and pricing:

```
MCP Tools (9 available)

FREE
  trader_my_stats              Score, rank, open positions
  trader_performance_report    Detailed scoring breakdown
  trader_last_trade            Most recent trade + total count

PAID (x402, USDC on Base)
  trader_get_leaderboard       Full rankings ($0.25+)
  trader_search_trader         Trader lookup ($0.02)
  trader_get_trade_history     Full trade log ($0.01/3 trades)

FREE (continued)
  trader_cancel_last           Cancel most recent trade (5-min window)
  trader_watch                 Watch a trader
  trader_unwatch               Stop watching a trader
```

4. Show MCP endpoint: `https://api.mangrovetraders.com/mcp/`
5. Show REST API docs: `https://api.mangrovetraders.com/api/docs`
