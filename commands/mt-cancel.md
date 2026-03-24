---
name: mt-cancel
description: Cancel your most recent trade (5-minute window)
---

# mt-cancel

Cancel the most recent trade. Only works within 5 minutes of submission.

## Steps

1. Ask for the trader's Twitter handle if not provided
2. Call the `trader_cancel_last` MCP tool with `twitter_handle`
3. If successful: show the cancelled trade details (symbol, action, quantity, price)
4. If `CANCEL_WINDOW_EXPIRED`: tell the user the window has passed, show how long ago the trade was
5. If `NO_TRADES`: tell the user no trades were found
6. If `TRADER_NOT_FOUND`: suggest they check the handle or make their first trade via `/mt-track`
