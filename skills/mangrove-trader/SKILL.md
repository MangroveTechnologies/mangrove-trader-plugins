---
name: mangrove-trader
description: >-
  Use when the user asks about trading, leaderboard, portfolio, performance,
  track a trade, log a buy or sell, check stats, rank, score, search for a
  trader, look up a trader, last trade, trade history, x402 payment, top
  traders, how am I doing, my rank, my score, my positions, open positions,
  cancel trade, watch trader, unwatch, follow trader.
version: 2.0.0
---

# MangroveTrader

Social trading leaderboard. Traders tweet to **@MangroveTrader** on Twitter, a Grok-powered agent parses trades, tracks positions against real market data, computes scoring metrics, and exposes rankings.

**10 MCP tools** -- 7 free, 3 paid via x402 (USDC on Base).
**13 commands** -- all prefixed with `/mt-`.

---

## Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/mt-track` | Compose a trade tweet | Free |
| `/mt-stats` | Score, rank, open positions | Free |
| `/mt-report` | Performance breakdown (return, Sharpe, drawdown) | Free |
| `/mt-last` | Most recent trade | Free |
| `/mt-history` | Trade history | Free (own) / x402 $0.01/3 trades (others) |
| `/mt-leaderboard` | Full rankings (top 5 free on Twitter) | x402 $0.25+ |
| `/mt-search` | Find a trader | x402 $0.02 |
| `/mt-cancel` | Cancel last trade (5-min window) | Free |
| `/mt-watch` | Watch a trader | Free |
| `/mt-unwatch` | Unwatch a trader | Free |
| `/mt-set-handle` | Set your Twitter handle for this session | Free |
| `/mt-status` | Server health + tool list | Free |
| `/mt-help` | List all commands | Free |

---

## Track a Trade

Trades are submitted by tweeting to @MangroveTrader on Twitter. Use `/mt-track` to compose the tweet.

### Tweet Format

| Asset Class | Example |
|-------------|---------|
| **Equities** | `enter long 100 AAPL @ 185.50` |
| **Crypto** | `enter long 2.5 BTC @ 64000` |
| **Futures** | `enter short 5 ES @ 5250` |
| **Options** | `enter long 10 AAPL 190C 2026-04-18 @ 3.50` |

**Actions:** `enter long`, `enter short`, `exit long`, `exit short`
**Shortcuts:** `long 100 AAPL` (defaults to `enter long`), `bought`, `sold`, `grabbed`, `dumped`, `faded`

---

## Authentication

Most free tools require identity verification via X OAuth 2.0. Check `MT_AUTH_TOKEN` env var first — if set, pass it as `auth_token`. If not set, call `trader_login` to get a verification URL.

**Tool:** `trader_login` (no params)
- Returns a URL — user opens it in a browser, authenticates with X, receives a token
- User sets `MT_AUTH_TOKEN=<token>` in their environment (persists for 30 days)
- Use `/mt-set-handle` to walk the user through this flow

---

## Free Tools

### My Stats -- `/mt-stats`

**Tool:** `trader_my_stats`

1. Check `MT_AUTH_TOKEN` env var. If set, pass as `auth_token`. If not, call `trader_login` and stop.
2. Call with `auth_token` (optional `twitter_handle` to verify the token matches a specific handle)
3. Returns: composite_score, rank, total_trades, qualified, open_positions

### Performance Report -- `/mt-report`

**Tool:** `trader_performance_report`

1. Check `MT_AUTH_TOKEN` env var. If set, pass as `auth_token`. If not, call `trader_login` and stop.
2. Call with `auth_token` and `timeframe` (daily/weekly/monthly/all_time/30d/7d, default: all_time)
3. Returns: composite_score, rank, total_return_pct, sharpe_ratio, max_drawdown_pct, win_rate, trade_count

### Last Trade -- `/mt-last`

**Tool:** `trader_last_trade`

1. Call with `twitter_handle` (public — no auth required)
2. Returns: action, symbol, asset_class, quantity, price, created_at, total_trades

---

## Paid Tools (x402)

All paid tools follow the x402 payment protocol. See [Payment Flow](#x402-payment-flow) below.

### Leaderboard -- `/mt-leaderboard`

**Tool:** `trader_get_leaderboard` -- $0.25+ USDC on Base. Top 5 free on Twitter.

1. Call WITHOUT `payment` param (include `timeframe` and `limit`)
2. Get PAYMENT_REQUIRED with price
3. Present price, confirm with user
4. If confirmed and payment signed, call WITH `payment`
5. Returns: ranked list of traders with score, return %, trade count

**Tip:** Top 5 is always free by tweeting "leaderboard" to @MangroveTrader.

### Search Trader -- `/mt-search`

**Tool:** `trader_search_trader` -- $0.02 USDC on Base

1. Call WITHOUT `payment` (include `query`)
2. Get PAYMENT_REQUIRED
3. Confirm with user
4. Call WITH `payment`
5. Returns: handle, display_name, score, rank, trade_count, qualified

### Trade History -- `/mt-history`

**Tool:** `trader_get_trade_history` -- Free (own) / $0.01 per 3 trades (others) USDC on Base

**Own history (free):**
1. Check `MT_AUTH_TOKEN` env var. If set, call with `twitter_handle` AND `auth_token` — data returns directly with `"access": "free"`.
2. Legacy fallback: `requester_handle` matching `twitter_handle` also grants free access.

**Others' history (paid):**
1. Call WITHOUT `payment` (include `twitter_handle`, optional `limit`)
2. Get PAYMENT_REQUIRED with total_trades and computed price
3. Present: "X trades available, cost is $Y USDC. Proceed?"
4. Call WITH `payment`
5. Returns: list of trades with action, symbol, asset_class, quantity, price, timestamp

---

## x402 Payment Flow

Paid tools use the [x402 protocol](https://www.x402.org/) for micropayments on Base (Coinbase L2) in USDC.

### Two-Step Flow

1. **Call WITHOUT `payment`** -- server returns PAYMENT_REQUIRED with:
   - `price`: cost in USDC
   - `payment_required`: base64-encoded x402 payment requirements
   - `payment_required_decoded`: human-readable requirements (network, address, amount)
2. **Present the price** to the user and ask for confirmation
3. **Sign and submit payment** -- requires an EVM wallet with USDC on Base
4. **Call WITH `payment`** -- pass the signed x402 payment header
5. **Present the data** from the successful response

### Payment Capability

**For agents with a wallet (autonomous agents):**
- Need an EVM wallet with USDC balance on Base network
- Use the x402 SDK to sign the payment against the requirements from step 1
- The MangroveMarkets TypeScript SDK (`@mangrove/sdk`) includes an x402 payment client

**For agents without a wallet (Claude Code users):**
- Free tools (mt-stats, mt-report, mt-last) work without payment
- For paid tools, present the price and suggest:
  - Use an API key (X-API-Key header bypasses x402 on REST endpoints)
  - Use the REST API directly at `https://api.mangrovetraders.com/api/x402/`
  - Check @MangroveTrader on Twitter for daily leaderboard updates

**API key access (bypasses x402):**
- Add `X-API-Key: <key>` header to REST requests
- API keys are issued to qualifying traders or by Mangrove Technologies
- API key holders get free access to all paid endpoints

### Payment Safety

- Payment is NOT charged if data retrieval fails
- Verify-then-settle: payment is verified before data fetch, settled only after successful response
- All transactions on Base (low gas, fast finality)

---

## Scoring Formula

| Component | Weight | Metric |
|-----------|--------|--------|
| Return | 50% | Total return percentage |
| Consistency | 30% | Sharpe ratio |
| Risk Management | 20% | Max drawdown (lower is better) |

Traders must close a minimum number of trades to qualify for scoring and the leaderboard. Scoring runs at midnight UTC daily.

---

## Tool Quick Reference

| Tool | Access | Price | Auth | Description |
|------|--------|-------|------|-------------|
| `trader_login` | Free | -- | None | Start X OAuth 2.0 — returns verification URL |
| `trader_my_stats` | Free | -- | `auth_token` required | Score, rank, open positions |
| `trader_performance_report` | Free | -- | `auth_token` required | Detailed scoring breakdown |
| `trader_last_trade` | Free | -- | None | Most recent trade + total count (public) |
| `trader_get_leaderboard` | x402 | $0.25+ | None | Full rankings. Top 5 free on Twitter. |
| `trader_search_trader` | x402 | $0.02 | None | Look up any trader by name/handle |
| `trader_get_trade_history` | Free / x402 | Free (own) / $0.01/3 (others) | `auth_token` for free own history | Trade log |
| `trader_cancel_last` | Free | -- | `auth_token` required | Cancel most recent trade |
| `trader_watch` | Free | -- | `auth_token` required | Watch a trader |
| `trader_unwatch` | Free | -- | `auth_token` required | Unwatch a trader |

---

## Endpoints

- **MCP**: `https://api.mangrovetraders.com/mcp/` (Streamable HTTP)
- **REST API docs**: `https://api.mangrovetraders.com/api/docs`
- **Health**: `https://api.mangrovetraders.com/health`
- **Twitter**: [@MangroveTrader](https://twitter.com/MangroveTrader)
