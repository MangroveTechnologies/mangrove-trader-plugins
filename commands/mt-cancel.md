---
name: mt-cancel
description: Cancel your most recent trade (5-minute window)
---

# mt-cancel

Cancel the most recent trade. Only works within 5 minutes of submission.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If set, use it as `auth_token` — do NOT ask for a Twitter handle.
2. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL and stop.
3. Call the `trader_cancel_last` MCP tool with `auth_token`.
   - **If MCP tool is not available**: this command requires the MCP connection. Suggest running `/mt-status` to check server health.
4. If successful: show the cancelled trade details (symbol, action, quantity, price)
5. If `CANCEL_WINDOW_EXPIRED`: tell the user the window has passed, show how long ago the trade was
6. If `NO_TRADES`: tell the user no trades were found
7. If `TRADER_NOT_FOUND`: suggest they check the handle or make their first trade via `/mt-track`
