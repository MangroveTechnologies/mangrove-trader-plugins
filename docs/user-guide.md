# MangroveTrader Plugin -- User Guide

Step-by-step guide to using every MangroveTrader feature through the Claude Code plugin.

**Prerequisites:**
- Claude Code installed
- This plugin installed (see [Install](#install) below)
- (Optional) A wallet with USDC on Base mainnet for paid tool testing (MetaMask, Phantom, or any EVM wallet)

**Cost:** Free to use most features. Your own trade history is free. Paid tools (others' history, full leaderboard, search) cost $0.02-$0.25+ USDC per query on Base.

---

## Install

```bash
git clone https://github.com/MangroveTechnologies/mangrove-trader-plugin.git
claude plugin marketplace add ./mangrove-trader-plugin
claude plugin install mangrove-trader
```

Or for a single session:
```bash
claude --plugin-dir ./mangrove-trader-plugin
```

Start Claude Code and verify the plugin loaded:
```
/mt-help
```

You should see all 13 commands listed. If you don't see `/mt-help`, the plugin didn't load -- check the install steps above.

---

## Step 1: Check Server Status

```
/mt-status
```

**Expected:** API health (healthy/unhealthy), Twitter Agent status (alive/dead), and a list of all 13 plugin commands.

**Pass criteria:**
- [ ] API shows "healthy"
- [ ] Twitter Agent shows "alive"
- [ ] 13 commands listed in user-journey order
- [ ] MCP endpoint shown: `https://api.mangrovetraders.com/mcp/`

---

## Step 2: Verify Your X Identity

```
/mt-set-handle
```

Most free tools require a verified session token tied to your X (Twitter) account. This step authenticates you via X OAuth 2.0 so your handle cannot be spoofed.

**Expected flow:**

1. Plugin checks for `MT_AUTH_TOKEN` environment variable
2. If not set: plugin calls `trader_login`, which returns a verification URL
3. Open the URL in your browser and authenticate with X
4. X redirects to the MangroveTrader callback, which issues a session token
5. Plugin instructs you to set `MT_AUTH_TOKEN=<token>` in your environment:
   - **macOS/zsh:** `export MT_AUTH_TOKEN=<token>` in `~/.zshenv`
   - **Linux/bash:** `export MT_AUTH_TOKEN=<token>` in `~/.bashrc`
   - **Windows:** `[System.Environment]::SetEnvironmentVariable('MT_AUTH_TOKEN', '<token>', 'User')`
6. Run `/mt-set-handle` again — plugin confirms: "Verified as @{handle}."

**If `MT_AUTH_TOKEN` is already set:** Plugin calls `trader_my_stats` to resolve and confirm your handle immediately.

**Pass criteria:**
- [ ] `trader_login` returns a valid X authorization URL
- [ ] After authenticating, token resolves to your correct handle
- [ ] "Verified as @{handle}" confirmation shown

**Note:** The session token expires in 30 days. Re-run `/mt-set-handle` after re-authenticating.

---

## Step 3: Look Up Your Stats (Free)

```
/mt-stats
```

**Expected:** Plugin reads `MT_AUTH_TOKEN`, calls `trader_my_stats` with `auth_token`, and shows:
- Composite score (0-100)
- Rank (# among all traders)
- Total trades
- Qualified status (true/false)
- Open position count

**Pass criteria:**
- [ ] MCP tool `trader_my_stats` was called (not a curl/REST fallback)
- [ ] `auth_token` was passed (no plain handle prompt)
- [ ] Response shows real data for your account
- [ ] If score is 0.0, that's normal -- scoring runs at midnight UTC

---

## Step 4: Get a Performance Report (Free)

```
/mt-report
```

Enter timeframe: `30d`

**Expected:** Plugin reads `MT_AUTH_TOKEN`, calls `trader_performance_report` with `auth_token` and `timeframe`, and shows:
- Composite score and rank
- Total return %
- Sharpe ratio (consistency)
- Max drawdown % (risk)
- Win rate and trade count
- Scoring weights (50% return, 30% consistency, 20% risk)

**Pass criteria:**
- [ ] MCP tool `trader_performance_report` was called
- [ ] `auth_token` was passed (no plain handle prompt)
- [ ] Timeframe reflected in response
- [ ] Scoring weights shown

---

## Step 5: Check Any Trader's Last Trade (Free)

```
/mt-last
```

Enter handle: `_jhthomas`

**Expected:** Plugin calls `trader_last_trade` (public — no auth required) and shows:
- Most recent trade (action, symbol, quantity, price, timestamp)
- Total trade count
- Mention of `/mt-history` for full history

**Pass criteria:**
- [ ] MCP tool `trader_last_trade` was called
- [ ] No auth token required — any handle works
- [ ] Trade details shown

---

## Step 6: Compose a Trade Tweet

```
/mt-track
```

Follow the prompts: action (long), quantity (100), symbol (AAPL), price (185.50)

**Expected:** The plugin composes a formatted tweet and tells you to post it to @MangroveTrader on Twitter.

**Pass criteria:**
- [ ] Output shows: "Tweet this to @MangroveTrader: long 100 AAPL @ 185.50"
- [ ] No MCP tool called (this is local tweet composition only)

**Note:** Trades are submitted via Twitter, not through the plugin. The plugin helps you format the tweet correctly.

---

## Step 7: View the Leaderboard (Paid -- $0.25+ USDC)

```
/mt-leaderboard
```

**Expected flow:**

1. Plugin calls `trader_get_leaderboard` WITHOUT payment
2. Server returns PAYMENT_REQUIRED with the price (e.g., "$0.25 for 100 rows")
3. Plugin presents the price and asks you to confirm

**If you have an x402-capable wallet:**
4. Confirm payment
5. Plugin signs the x402 payment using your wallet (USDC on Base)
6. Plugin calls again WITH the signed payment
7. Full leaderboard displayed with rank, handle, score, return %

**If you don't have a wallet:**
4. Plugin tells you the price and suggests alternatives:
   - Your own rank is free via `/mt-stats`
   - Use the REST API with an API key (`X-API-Key` header bypasses payment)
   - Daily top 10 posted on @MangroveTrader Twitter

**Pass criteria:**
- [ ] First call returns PAYMENT_REQUIRED (not data)
- [ ] Price is presented before any charge
- [ ] Free alternative suggested if payment declined

### How to pay with MetaMask or Phantom

The x402 payment flow works like this:

1. The plugin shows you the payment requirements: amount, network (Base), currency (USDC), recipient address
2. If your agent has a configured wallet, it signs the payment automatically
3. If not, you can pay manually:
   - Open MetaMask/Phantom
   - Switch to Base network
   - The plugin will show the exact USDC amount and recipient
   - Send the USDC transfer
   - The plugin uses the transaction to complete the tool call

**Note:** Most Claude Code users won't have wallet signing built into their session. The free tools + API key path is the practical option for human users. The x402 flow is designed for autonomous agents with configured wallets.

---

## Step 8: Search for a Trader (Paid -- $0.02 USDC)

```
/mt-search
```

Enter a search query (handle or name).

**Expected:** Same two-step payment flow as leaderboard. Price: $0.02 flat.

**Pass criteria:**
- [ ] PAYMENT_REQUIRED returned first
- [ ] $0.02 price shown
- [ ] Results show handle, score, rank, trade count if payment completed

---

## Step 9: View Trade History (Free for own, Paid for others)

```
/mt-history
```

Enter handle: your own handle (for free access)

**Own history (free):**
- Plugin reads `MT_AUTH_TOKEN` and calls `trader_get_trade_history` with `auth_token`
- Data returns directly with `"access": "free"` — no payment needed

**Others' history (paid, $0.01 per 3 trades):**
- Same two-step payment flow. Price depends on number of trades.

**Pass criteria:**
- [ ] Own history returns data immediately (no PAYMENT_REQUIRED)
- [ ] Own history response has `access: "free"`
- [ ] `auth_token` used for free access (not plain handle matching)
- [ ] Others' history shows PAYMENT_REQUIRED with computed price
- [ ] Price formula: ceil(trades / 3) * $0.01
- [ ] Full trade list returned if payment completed

---

## Step 10: Cancel a Trade (Free)

```
/mt-cancel
```

**Expected:** Plugin reads `MT_AUTH_TOKEN`, calls `trader_cancel_last` with `auth_token`:
- If you have a trade within the last 5 minutes: trade cancelled, details shown
- If your last trade was more than 5 minutes ago: `CANCEL_WINDOW_EXPIRED` error with how long ago the trade was
- If you have no trades: `NO_TRADES` error

**Pass criteria:**
- [ ] MCP tool `trader_cancel_last` was called
- [ ] `auth_token` passed (no handle prompt)
- [ ] 5-minute window enforced
- [ ] Structured error for expired/no trades (no crash)

---

## Step 11: Watch a Trader (Free)

```
/mt-watch
```

Enter the target trader's handle.

**Expected:** Plugin reads `MT_AUTH_TOKEN`, calls `trader_watch` with `auth_token` and `target_handle`:
- Success: "Now watching @target. You watch N trader(s)."
- Plus a note: "Watchlist saved. Activity notifications for watched traders are coming soon."

**What watching does today:** Saves the relationship in MangroveTrader's database. Activity notifications for watched traders are planned but not yet available.

**Pass criteria:**
- [ ] MCP tool `trader_watch` was called
- [ ] `auth_token` passed (no watcher handle prompt)
- [ ] Confirmation with watch count
- [ ] "notifications coming soon" note present
- [ ] Self-watch rejected with `SELF_WATCH` error
- [ ] Non-trader watcher rejected with `NOT_A_TRADER` error

---

## Step 12: Unwatch a Trader (Free)

```
/mt-unwatch
```

Enter the target trader's handle.

**Expected:** Plugin reads `MT_AUTH_TOKEN`, calls `trader_unwatch` with `auth_token` and `target_handle`. Confirms: "Stopped watching @target."

**Pass criteria:**
- [ ] MCP tool `trader_unwatch` was called
- [ ] `auth_token` passed (no handle prompt)
- [ ] Confirmation shown

---

## Step 13: List All Commands

```
/mt-help
```

**Expected:** All 13 commands listed in user-journey order (trade, stats, report, history, leaderboard, search, manage, utility), with pricing for paid commands.

**Pass criteria:**
- [ ] 13 commands shown
- [ ] Pricing shown for paid commands
- [ ] Own trade history noted as free

---

## Summary

| # | Test | Command | MCP Tool | Auth | Cost |
|---|------|---------|----------|------|------|
| 1 | Server status | `/mt-status` | (health endpoint) | None | Free |
| 2 | Verify identity | `/mt-set-handle` | `trader_login` | X OAuth | Free |
| 3 | Trader stats | `/mt-stats` | `trader_my_stats` | `auth_token` | Free |
| 4 | Performance report | `/mt-report` | `trader_performance_report` | `auth_token` | Free |
| 5 | Last trade | `/mt-last` | `trader_last_trade` | None | Free |
| 6 | Compose trade | `/mt-track` | (local only) | None | Free |
| 7 | Leaderboard | `/mt-leaderboard` | `trader_get_leaderboard` | None | $0.25+ (top 5 free on Twitter) |
| 8 | Search trader | `/mt-search` | `trader_search_trader` | None | $0.02 |
| 9 | Trade history | `/mt-history` | `trader_get_trade_history` | `auth_token` (own) | Free (own) / $0.01/3 trades (others) |
| 10 | Cancel trade | `/mt-cancel` | `trader_cancel_last` | `auth_token` | Free |
| 11 | Watch trader | `/mt-watch` | `trader_watch` | `auth_token` | Free |
| 12 | Unwatch trader | `/mt-unwatch` | `trader_unwatch` | `auth_token` | Free |
| 13 | Help | `/mt-help` | (local only) | None | Free |

**Total cost to test everything:** $0.27+ USDC (if you test all 3 paid tools with minimum params). Free tools cost nothing.
