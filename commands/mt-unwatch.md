---
name: mt-unwatch
description: Remove a trader from your watchlist
---

# mt-unwatch

Remove a trader from your watchlist. See `/mt-watch` for details on what the watchlist does.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If set, use it as `auth_token` — do NOT ask for your Twitter handle.
2. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL and stop.
3. Ask for the target trader's Twitter handle.
4. Call the `trader_unwatch` MCP tool with `auth_token` and `target_handle`.
   - **If MCP tool is not available**: this command requires the MCP connection. Suggest running `/mt-status` to check server health.
5. If successful: show confirmation
6. If `NOT_A_TRADER`: tell the user they need to make a trade first
7. If `TRADER_NOT_FOUND`: the target doesn't exist
