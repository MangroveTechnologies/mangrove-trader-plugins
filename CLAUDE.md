# MangroveTrader Plugin

## Default Persona

When working in this repo, you are the **product owner**. Read `.claude/agents/product-owner.md` for your full agent spec and follow it. Load your memory from the repo memory directory on every session start.

---

Claude Code plugin for the MangroveTrader social trading leaderboard.

## Structure

```
.claude-plugin/plugin.json    Plugin manifest (required for marketplace)
.mcp.json                     MCP server config (remote, streamable HTTP)
skills/mangrove-trader/       Consolidated skill for all 7 tool interactions
commands/                     Slash commands (status, track, stats)
hooks/                        Context injection on prompt submit
```

## MCP Server

The plugin connects to the MangroveTrader MCP server via streamable HTTP. The server URL is configured in `.mcp.json`. No local process is needed -- the server runs on GCP Cloud Run.

## Tools (6 total)

**Free (no auth):** `trader_my_stats`, `trader_performance_report`, `trader_last_trade`
**Paid (x402):** `trader_get_leaderboard` ($0.25+), `trader_search_trader` ($0.02), `trader_get_trade_history` ($0.01/3 trades)

## x402 Payment Convention

Paid tools follow a two-step flow:
1. Call WITHOUT `payment` parameter -- server returns PAYMENT_REQUIRED with price
2. Present price to user, ask to confirm
3. Call WITH `payment` parameter (value from step 1 response)

Never skip the confirmation step. Never hardcode prices -- always read from the PAYMENT_REQUIRED response.

## Trade Tracking

Trades are logged by tweeting to @MangroveTrader on Twitter. This plugin does NOT submit trades directly -- it helps users compose the tweet format.
