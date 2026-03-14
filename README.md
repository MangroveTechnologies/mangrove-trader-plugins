# MangroveTrader Plugins

Claude Code + OpenClaw plugins for [MangroveTrader](https://github.com/MangroveTechnologies/MangroveTrader) -- a social trading leaderboard where traders post trades via Twitter (@MangroveTrader).

## Install (Claude Code)

Clone this repo and point Claude Code at the `.claude/` directory. Set `MANGROVE_TRADER_URL` to your server.

## Install (OpenClaw)

```bash
cd openclaw-plugin && npm install
```

## Available Skills

| Skill | Pricing | Description |
|-------|---------|-------------|
| track-trade | Free | Compose tweets for @MangroveTrader |
| my-portfolio | Free | Check your score, rank, positions |
| performance | Free | Detailed scoring breakdown |
| leaderboard | $0.25 USDC | Full top 100 leaderboard |
| search-trader | $0.02 USDC | Look up any trader |

## x402 Payment

Paid skills use x402 micropayments on Base (USDC). The skill calls the tool without payment first to get the price, asks you to confirm, then calls with payment.

## Configuration

- `MANGROVE_TRADER_URL` -- MCP server URL (default: http://localhost:8080)
- `MANGROVE_TRADER_API_KEY` -- API key (optional)
