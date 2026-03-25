# MangroveTrader Plugin

## Default Persona

When working in this repo, you are the **product owner**. Read `.claude/agents/product-owner.md` for your full agent spec and follow it. Load your memory from the repo memory directory on every session start.

---

Claude Code plugin for the MangroveTrader social trading leaderboard.

## Structure

```
.claude-plugin/
  plugin.json                 Plugin manifest (required for marketplace)
  marketplace.json            Marketplace index (required for claude plugin install)
.mcp.json                     MCP server config (remote, streamable HTTP)
skills/mangrove-trader/       Consolidated skill for all tool interactions
commands/                     12 mt-* slash commands
hooks/                        Context injection on prompt submit
docs/plans/                   Implementation plans
```

## Commands (12 total, all prefixed /mt-)

**Free:** `/mt-stats`, `/mt-report`, `/mt-last`, `/mt-track`, `/mt-status`, `/mt-help`
**Paid (x402):** `/mt-leaderboard`, `/mt-search`, `/mt-history`
**Free actions:** `/mt-cancel`, `/mt-watch`, `/mt-unwatch`

## MCP Server

The plugin connects to the MangroveTrader MCP server via streamable HTTP at `https://api.mangrovetraders.com/mcp/`. No local process needed -- the server runs on GCP Cloud Run.

## Tools (9 available)

**Free:** `trader_my_stats`, `trader_performance_report`, `trader_last_trade`
**Paid (x402):** `trader_get_leaderboard` ($0.25+), `trader_search_trader` ($0.02), `trader_get_trade_history` ($0.01/3 trades)
**Free actions:** `trader_cancel_last`, `trader_watch`, `trader_unwatch`

## x402 Payment Flow

Paid tools use the x402 protocol (USDC on Base):

1. Call tool WITHOUT `payment` -- get PAYMENT_REQUIRED with price and requirements
2. Present price to user, ask to confirm
3. Agent signs x402 payment (requires EVM wallet with USDC on Base) OR user uses API key on REST
4. Call tool WITH signed `payment` parameter
5. Present data

Never skip the confirmation step. Never hardcode prices. API key holders (X-API-Key header on REST) bypass x402.

## Trade Tracking

Trades are logged by tweeting to @MangroveTrader on Twitter. This plugin does NOT submit trades directly -- `/mt-track` helps users compose the tweet format.
