# MangroveTrader Plugin for Claude Code

[MangroveTrader](https://mangrovetraders.com) is a social trading leaderboard where traders post trades on Twitter, positions are tracked against real market data, and performance is scored daily.

This plugin connects Claude Code to the MangroveTrader MCP server, giving you 13 slash commands and 10 MCP tools for stats, leaderboard, trade history, and more.

**Website:** [mangrovetraders.com](https://mangrovetraders.com)
**Twitter:** [@MangroveTrader](https://twitter.com/MangroveTrader)
**Source:** [github.com/MangroveTechnologies/mangrove-trader-plugin](https://github.com/MangroveTechnologies/mangrove-trader-plugin)

## Install

```bash
git clone https://github.com/MangroveTechnologies/mangrove-trader-plugin.git
claude plugin marketplace add ./mangrove-trader-plugin
claude plugin install mangrove-trader
```

Or load for a single session without installing:

```bash
claude --plugin-dir ./mangrove-trader-plugin
```

## Commands

All commands are prefixed with `/mt-`:

| Command | Description | Access |
|---------|-------------|--------|
| `/mt-track` | Compose a trade tweet | Free |
| `/mt-stats` | Your score, rank, open positions | Free |
| `/mt-report` | Performance breakdown (return, Sharpe, drawdown) | Free |
| `/mt-last` | Most recent trade and total count | Free |
| `/mt-history` | Trade history | Free (own) / Paid $0.01/3 trades (others) |
| `/mt-leaderboard` | Full rankings (top 5 free on Twitter) | Paid ($0.25+ USDC) |
| `/mt-search` | Find a trader by handle or name | Paid ($0.02 USDC) |
| `/mt-cancel` | Cancel last trade (5-min window) | Free |
| `/mt-watch` | Watch a trader | Free |
| `/mt-unwatch` | Unwatch a trader | Free |
| `/mt-set-handle` | Set your Twitter handle for this session | Free |
| `/mt-status` | Server health | Free |
| `/mt-help` | List all commands | Free |

## MCP Tools

The plugin connects to MangroveTrader's MCP server at `https://api.mangrovetraders.com/mcp/`. 10 tools available:

| Tool | Access | Price | Notes |
|------|--------|-------|-------|
| `trader_login` | Free | -- | Start X OAuth 2.0 — returns a verification URL |
| `trader_my_stats` | Free | -- | Requires `auth_token` (MT_AUTH_TOKEN) |
| `trader_performance_report` | Free | -- | Requires `auth_token` |
| `trader_last_trade` | Free | -- | Public — accepts any `twitter_handle` |
| `trader_cancel_last` | Free | -- | Requires `auth_token` |
| `trader_watch` | Free | -- | Requires `auth_token` |
| `trader_unwatch` | Free | -- | Requires `auth_token` |
| `trader_get_leaderboard` | x402 | $0.25+ USDC | Top 5 free on Twitter |
| `trader_search_trader` | x402 | $0.02 USDC | -- |
| `trader_get_trade_history` | Free / x402 | Free (own w/ auth_token) / $0.01/3 trades (others) | -- |

## How Trading Works

1. Tweet your trade to **@MangroveTrader** on Twitter (use `/mt-track` to compose)
2. A Grok-powered agent parses your trade and tracks the position
3. Positions are marked-to-market against real prices every 5 minutes
4. Scoring runs daily at midnight UTC

### Tweet Format

```
@MangroveTrader long 100 AAPL @ 185.50       # Equities
@MangroveTrader enter long 2.5 BTC @ 64000   # Crypto
@MangroveTrader exit short 5 ES @ 5250       # Futures
```

### Scoring

| Component | Weight | Metric |
|-----------|--------|--------|
| Return | 50% | Total return percentage |
| Consistency | 30% | Sharpe ratio |
| Risk Management | 20% | Max drawdown (lower is better) |

## x402 Payments

Paid tools use the [x402 protocol](https://www.x402.org/) for micropayments:

- **Network:** Base (Coinbase L2)
- **Currency:** USDC
- **Flow:** Call without payment -> see price -> confirm -> sign payment -> call with payment
- **Safety:** You are never charged if data retrieval fails
- **API key bypass:** `X-API-Key` header on REST endpoints skips x402

For agents with wallets: use the x402 SDK or MangroveMarkets TypeScript SDK to sign payments.
For Claude Code users without wallets: free tools work without payment. Paid data available via REST API with an API key.

## Security and Privacy

This plugin connects to a remote MCP server hosted on GCP Cloud Run. Here is what it does and does not do:

- **Data accessed:** Public trading data (scores, ranks, trade history). No personally identifiable information.
- **Identity verification:** Free tools that write or read your account (`trader_my_stats`, `trader_cancel_last`, `trader_watch`, `trader_unwatch`) require a session token obtained via X OAuth 2.0. Use `/mt-set-handle` to authenticate — your handle is verified server-side and cannot be spoofed.
- **No credentials stored:** The plugin does not store, transmit, or require any API keys, wallet keys, or passwords. The session token (`MT_AUTH_TOKEN`) is stored only in your local environment.
- **Payment confirmation:** Paid tools always show the price and ask for confirmation before any charge. You are never charged without explicit consent.
- **x402 payments:** All payments settle on Base mainnet (USDC). Transaction hashes are returned for on-chain verification.
- **Server source code:** The MCP server source is public at [github.com/MangroveTechnologies/MangroveTrader](https://github.com/MangroveTechnologies/MangroveTrader).
- **No tracking:** The plugin does not track usage, analytics, or telemetry beyond what the MCP server logs for rate limiting.

## Documentation

- [User Guide](docs/user-guide.md) -- Step-by-step walkthrough of every feature
- [MangroveTrader Website](https://mangrovetraders.com) -- Landing page with full docs
- [API Reference](https://mangrovetraders.com/docs/api-reference) -- REST and MCP endpoint details
- [Twitter Validation Checklist](https://github.com/MangroveTechnologies/MangroveTrader/blob/main/docs/reports/twitter-validation-checklist.md) -- Test every feature on Twitter

## License

MIT
