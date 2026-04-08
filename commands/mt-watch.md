---
name: mt-watch
description: Add a trader to your watchlist (activity notifications coming soon)
---

# mt-watch

Add a trader to your watchlist. This saves the relationship for future use -- activity notifications for watched traders are planned but not yet available.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If set, use it as `auth_token` — do NOT ask for your Twitter handle.
2. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL and stop.
3. Ask for the target trader's Twitter handle.
4. Call the `trader_watch` MCP tool with `auth_token` and `target_handle`.
   - **If MCP tool is not available**: this command requires the MCP connection. Suggest running `/mt-status` to check server health.
5. If successful: show confirmation and current watch count
6. If `SELF_WATCH`: tell the user they can't watch themselves
7. If `NOT_A_TRADER`: tell the user they need to make a trade first via `/mt-track`
8. If `TRADER_NOT_FOUND`: the target doesn't exist, suggest `/mt-search` to find them
