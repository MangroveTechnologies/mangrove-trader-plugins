---
name: mt-last
description: Show any trader's most recent trade and total trade count (free, no auth required)
---

# mt-last

Show a trader's most recent trade. Free for anyone — no login required.

## Steps

1. Ask for the Twitter handle to look up if not provided.
2. Call the `trader_last_trade` MCP tool with `twitter_handle`.
3. **If MCP tool is not available**, fall back to REST: `POST https://api.mangrovetraders.com/api/v1/trader/last_trade` with `{"twitter_handle": "<handle>"}`
4. Present the most recent trade:
   - **Action** (enter_long, enter_short, exit_long, exit_short)
   - **Symbol** and **Asset Class**
   - **Quantity** and **Price**
   - **Timestamp**
   - **Total trade count**
5. Mention that full trade history is available via `/mt-history` (free for your own with auth, $0.01/3 trades for others)
