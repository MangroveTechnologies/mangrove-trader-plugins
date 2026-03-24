# MangroveTrader Plugin for Claude Code

Social trading leaderboard plugin. Track trades via [@MangroveTrader](https://twitter.com/MangroveTrader) on Twitter, check your stats and performance for free, and access full rankings and trader search via x402 micropayments.

## Install

From source (GitHub):

```bash
git clone https://github.com/MangroveTechnologies/mangrove-trader-plugins.git
claude plugin marketplace add ./mangrove-trader-plugins
claude plugin install mangrove-trader
```

Or load for a single session without installing:

```bash
claude --plugin-dir ./mangrove-trader-plugins
```

## Commands

All commands are prefixed with `/mt-`:

| Command | Description | Access |
|---------|-------------|--------|
| `/mt-stats` | Your score, rank, and open positions | Free |
| `/mt-report` | Detailed performance breakdown (return, Sharpe, drawdown) | Free |
| `/mt-last` | Most recent trade and total count | Free |
| `/mt-leaderboard` | Full leaderboard rankings | Paid ($0.25+ USDC) |
| `/mt-search` | Find a trader by handle or name | Paid ($0.02 USDC) |
| `/mt-history` | Complete trade history | Paid ($0.01/3 trades) |
| `/mt-track` | Compose a trade tweet for @MangroveTrader | Free |
| `/mt-cancel` | Cancel your last trade (5-min window) | Free |
| `/mt-watch` | Watch a trader's activity | Free |
| `/mt-unwatch` | Stop watching a trader | Free |
| `/mt-status` | Server health and tool availability | Free |
| `/mt-help` | List all commands | Free |

## MCP Tools

The plugin connects to MangroveTrader's MCP server. 9 tools available.

| Tool | Access | Price |
|------|--------|-------|
| `trader_my_stats` | Free | -- |
| `trader_performance_report` | Free | -- |
| `trader_last_trade` | Free | -- |
| `trader_get_leaderboard` | x402 | $0.25+ USDC |
| `trader_search_trader` | x402 | $0.02 USDC |
| `trader_get_trade_history` | x402 | $0.01/3 trades |

## How Trading Works

1. Tweet your trade to **@MangroveTrader** on Twitter (use `/mt-track` to compose)
2. A Grok-powered agent parses your trade and tracks the position
3. Positions are marked-to-market against real prices every 5 minutes
4. Scoring runs daily at midnight UTC: 50% return, 30% consistency (Sharpe), 20% risk (max drawdown)

### Tweet Format

```
enter long 100 AAPL @ 185.50       # Equities
enter long 2.5 BTC @ 64000         # Crypto
enter short 5 ES @ 5250            # Futures
enter long 10 AAPL 190C 2026-04-18 @ 3.50  # Options
```

## x402 Payments

Paid tools use the [x402 protocol](https://www.x402.org/) for micropayments:

- **Network:** Base (Coinbase L2)
- **Currency:** USDC
- **Flow:** Call without payment -> see price -> confirm -> sign payment -> call with payment
- **Safety:** You are never charged if data retrieval fails
- **API key bypass:** `X-API-Key` header on REST endpoints skips x402

For agents with wallets: use the x402 SDK or MangroveMarkets TypeScript SDK.
For Claude Code users without wallets: free tools work without payment. Paid data available via REST API with an API key.

## License

MIT
