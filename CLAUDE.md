# MangroveTrader Plugins

Claude Code + OpenClaw plugins for MangroveTrader social trading leaderboard (@MangroveTrader).

## Structure

- `.claude/skills/` -- Claude Code skills (one per interaction)
- `.claude/commands/` -- Slash commands
- `.claude/hooks/` -- Lifecycle hooks
- `openclaw-plugin/` -- OpenClaw plugin with tool proxies
- `shared/` -- Config and types

## Rules

- Trades logged via Twitter only. track-trade skill helps compose tweets.
- x402 paid skills: call without payment, present price, call with payment.
- Error responses: {error, code, message, suggestion}
- Server: MANGROVE_TRADER_URL env var, default localhost:8080
- Twitter: @MangroveTrader
