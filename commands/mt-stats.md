---
name: mt-stats
description: Look up a trader's stats -- score, rank, trade count, and open positions (free)
---

# mt-stats

Look up a trader's stats on MangroveTrader.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If set, use it as `auth_token` — do NOT ask for a Twitter handle.
2. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL and stop — do not fall back to asking for a handle.
3. Call the `trader_my_stats` MCP tool with `auth_token`.
4. **If MCP tool is not available**, fall back to REST: `POST https://api.mangrovetraders.com/api/v1/trader/my_stats` with `{"auth_token": "<token>"}`
5. Present results:
   - **Composite Score** (0-100)
   - **Rank** (among all traders, 0 = unranked)
   - **Total Trades**
   - **Qualified** (true/false -- minimum trade count required for leaderboard)
   - **Open Positions** count
6. If score is 0.0, note that scoring runs at midnight UTC daily
7. Suggest `/mt-report` for a detailed performance breakdown
