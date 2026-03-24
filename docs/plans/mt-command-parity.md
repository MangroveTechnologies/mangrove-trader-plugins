# mt-* Command Parity Plan

Full command parity between MangroveTrader Twitter agent (12 capabilities) and the Claude Code plugin.

## Current State

**Plugin:** 3 commands (`/stats`, `/status`, `/track`), 1 skill (`mangrove-trader`), context hook.
**Server:** 6 MCP tools (3 free, 3 x402). Cancel, watch, unwatch exist only as Twitter command handlers -- no MCP tools, no REST endpoints.

## Target State

12 `mt-*` prefixed commands covering every MangroveTrader capability.

| # | Command | Maps to | Access | Phase |
|---|---------|---------|--------|-------|
| 1 | `/mt-stats` | `trader_my_stats` | Free | 1 (rename) |
| 2 | `/mt-report` | `trader_performance_report` | Free | 1 (rename) |
| 3 | `/mt-last` | `trader_last_trade` | Free | 1 (rename) |
| 4 | `/mt-track` | Tweet composition (no MCP tool) | Free | 1 (rename) |
| 5 | `/mt-status` | `GET /health` + tool listing | Free | 1 (rename) |
| 6 | `/mt-leaderboard` | `trader_get_leaderboard` | x402 $0.25+ | 1 (new) |
| 7 | `/mt-search` | `trader_search_trader` | x402 $0.02 | 1 (new) |
| 8 | `/mt-history` | `trader_get_trade_history` | x402 $0.01/3 | 1 (new) |
| 9 | `/mt-help` | Local (no tool call) | Free | 1 (new) |
| 10 | `/mt-cancel` | `trader_cancel_last` (new) | Free | 3 |
| 11 | `/mt-watch` | `trader_watch` (new) | Free | 3 |
| 12 | `/mt-unwatch` | `trader_unwatch` (new) | Free | 3 |

---

## Phase 1 -- Plugin-Side (No Server Changes)

**Goal:** 8 working commands using existing MCP tools + local logic.
**Dependencies:** None. All tools already exist on the server.
**Delegate to:** `backend-developer` for command file creation.

### 1a. Rename existing commands

Delete old files, create new ones with `mt-` prefix. Content stays the same with updated cross-references.

| Old File | New File | Changes |
|----------|----------|---------|
| `commands/stats.md` | `commands/mt-stats.md` | Rename, update `name: mt-stats`, cross-refs point to mt-* commands |
| `commands/status.md` | `commands/mt-status.md` | Rename, update `name: mt-status`, update tool table to include all 12 commands |
| `commands/track.md` | `commands/mt-track.md` | Rename, update `name: mt-track` |

**Files to delete:** `commands/stats.md`, `commands/status.md`, `commands/track.md`
**Files to create:** `commands/mt-stats.md`, `commands/mt-status.md`, `commands/mt-track.md`

### 1b. Create commands for existing MCP tools

Three new commands wrapping x402-gated MCP tools. Each must implement the two-step x402 payment flow (call without payment, present price, confirm, call with payment).

#### `/mt-leaderboard` -- `commands/mt-leaderboard.md`

```yaml
---
name: mt-leaderboard
description: View the MangroveTrader leaderboard (x402 paid, $0.25+ USDC on Base)
---
```

Steps:
1. Ask for optional timeframe (daily/weekly/monthly/all_time/30d/7d, default: all_time) and limit (1-500, default: 100)
2. Call `trader_get_leaderboard` WITHOUT `payment` param
3. Present price from PAYMENT_REQUIRED response, ask user to confirm
4. If confirmed, call WITH `payment` param
5. Present leaderboard: rank, handle, score, return %
6. If declined, suggest `/mt-stats` (free, shows own rank) or @MangroveTrader Twitter (daily top 10)

#### `/mt-search` -- `commands/mt-search.md`

```yaml
---
name: mt-search
description: Search for a trader by handle or name (x402 paid, $0.02 USDC on Base)
---
```

Steps:
1. Ask for search query (handle or display name)
2. Call `trader_search_trader` WITHOUT `payment`
3. Present $0.02 cost, ask to confirm
4. If confirmed, call WITH `payment`
5. Present results: handle, display name, score, rank, trade count, qualified status
6. If declined, suggest `/mt-stats` with exact handle if known

#### `/mt-history` -- `commands/mt-history.md`

```yaml
---
name: mt-history
description: View a trader's full trade history (x402 paid, $0.01 per 3 trades USDC on Base)
---
```

Steps:
1. Ask for Twitter handle and optional trade limit (0 = all, max 1000)
2. Call `trader_get_trade_history` WITHOUT `payment`
3. Present total available trades and computed price, ask to confirm
4. If confirmed, call WITH `payment`
5. Present trades: action, symbol, asset class, quantity, price, timestamp
6. If declined, suggest `/mt-last` (free, shows most recent trade only)

### 1c. Create local commands (no MCP tool needed)

#### `/mt-help` -- `commands/mt-help.md`

```yaml
---
name: mt-help
description: Show all MangroveTrader plugin commands
---
```

Steps:
1. Display all 12 commands in a formatted table (9 available in Phase 1, 3 marked as "coming soon")
2. Group by category: Free Stats, Paid Data, Trade Actions, Utility
3. Include brief pricing info for x402 commands
4. Mention that trades are submitted via Twitter (@MangroveTrader)

Content to display:

```
MangroveTrader Plugin Commands

FREE STATS
  /mt-stats        Your score, rank, and open positions
  /mt-report       Detailed performance breakdown (return, sharpe, drawdown)
  /mt-last         Your most recent trade

PAID DATA (x402, USDC on Base)
  /mt-leaderboard  Full rankings ($0.25+)
  /mt-search       Find a trader ($0.02)
  /mt-history      Trade history ($0.01/3 trades)

TRADE ACTIONS
  /mt-track        Compose a trade tweet for @MangroveTrader
  /mt-cancel       Cancel your last trade (5-min window) [coming soon]

SOCIAL
  /mt-watch        Watch a trader's activity [coming soon]
  /mt-unwatch      Stop watching a trader [coming soon]

UTILITY
  /mt-status       Server health and tool availability
  /mt-help         This help message
```

### 1d. Update `/mt-status` to reflect full command set

Update the tool/pricing table in `mt-status.md` to list all 12 commands and 9 MCP tools (6 existing + 3 coming in Phase 2).

### Phase 1 Acceptance Criteria

- [ ] 8 command files exist in `commands/` with `mt-` prefix
- [ ] Old command files (`stats.md`, `status.md`, `track.md`) deleted
- [ ] All cross-references between commands use `mt-*` names
- [ ] x402 commands (mt-leaderboard, mt-search, mt-history) document the two-step payment flow
- [ ] mt-help lists all 12 commands with coming-soon markers for Phase 3 commands
- [ ] mt-status shows updated tool table
- [ ] Plugin still connects to `https://api.mangrovetraders.com/mcp/` (no .mcp.json changes)
- [ ] hooks/context.json updated to reference mt-* command names

---

## Phase 2 -- Server-Side (MangroveTrader Repo)

**Goal:** 3 new MCP tools: `trader_cancel_last`, `trader_watch`, `trader_unwatch`.
**Repo:** MangroveTechnologies/MangroveTrader
**Dependencies:** None (handlers already exist in `src/worker/handlers/commands.py`).
**Delegate to:** `backend-developer` (MangroveTrader product owner coordinates).

### Server Implementation Details

The Twitter agent already has working handler functions. The MCP tools need to expose the same logic via the MCP protocol.

#### Reference: Existing handler signatures

```python
# src/worker/handlers/commands.py
async def handle_cancel(db, author_handle, tweet_id, get_convo_client=None) -> str
async def handle_watch(db, author_handle, target_handle) -> str
async def handle_unwatch(db, author_handle, target_handle) -> str
```

#### 2a. `trader_cancel_last` -- Cancel most recent trade

**File:** `src/mcp/tools_trader.py` (add to free tools module)

Parameters:
- `twitter_handle` (str, required): The trader's Twitter handle

Logic:
1. Look up trader by handle
2. Get most recent trade
3. Check if within 5-minute cancel window (`CANCEL_WINDOW_MINUTES`)
4. If expired, return error message (no LLM witty rejection -- that's Twitter-only)
5. If within window, delete the trade and replay position if needed
6. Return: cancelled trade details (symbol, action, quantity, price) or error

Note: The Twitter handler uses `tweet_id` for trade lookup, but the MCP tool should use `trader_id` + most recent trade. The LLM witty rejection on timeout is Twitter-specific; the MCP tool returns a plain error with the cancel window duration.

#### 2b. `trader_watch` -- Watch a trader

**File:** `src/mcp/tools_trader.py` (add to free tools module)

Parameters:
- `twitter_handle` (str, required): The watcher's handle (the user)
- `target_handle` (str, required): The trader to watch

Logic:
1. Look up both traders
2. Validate not self-watching
3. Call `db.follow_trader(watcher_id, target_id)`
4. Return: confirmation with current watch count

#### 2c. `trader_unwatch` -- Stop watching a trader

**File:** `src/mcp/tools_trader.py` (add to free tools module)

Parameters:
- `twitter_handle` (str, required): The watcher's handle
- `target_handle` (str, required): The trader to unwatch

Logic:
1. Look up both traders
2. Call `db.unfollow_trader(watcher_id, target_id)`
3. Return: confirmation

#### 2d. Register tools in MCP server

**File:** `src/mcp/registry.py` -- Add the 3 new tools to the tool registry.

### Phase 2 Acceptance Criteria

- [ ] 3 new MCP tools registered and callable via `https://api.mangrovetraders.com/mcp/`
- [ ] `trader_cancel_last` enforces 5-minute cancel window
- [ ] `trader_watch` prevents self-watching, requires watcher to have at least 1 trade
- [ ] `trader_unwatch` handles "not found" gracefully
- [ ] All 3 tools are free (no x402 gating)
- [ ] Existing 6 tools unaffected (regression check)
- [ ] Tests added for each new tool
- [ ] Deployed to Cloud Run (MangroveTrader CI/CD)
- [ ] GitHub issue created in MangroveTrader repo to track this work

---

## Phase 3 -- Plugin-Side (After Phase 2 Deploys)

**Goal:** 3 final commands completing the 12-command set.
**Dependencies:** Phase 2 deployed and verified.
**Delegate to:** `backend-developer`

### 3a. `/mt-cancel` -- `commands/mt-cancel.md`

```yaml
---
name: mt-cancel
description: Cancel your most recent trade (5-minute window)
---
```

Steps:
1. Ask for Twitter handle if not known
2. Call `trader_cancel_last` with `twitter_handle`
3. If successful: show cancelled trade details (symbol, action, quantity, price)
4. If expired: show error with cancel window duration
5. If no trades: show "no trades found" message

### 3b. `/mt-watch` -- `commands/mt-watch.md`

```yaml
---
name: mt-watch
description: Watch a trader to follow their activity
---
```

Steps:
1. Ask for the user's Twitter handle if not known
2. Ask for the target trader's handle
3. Call `trader_watch` with both handles
4. Show confirmation and current watch count

### 3c. `/mt-unwatch` -- `commands/mt-unwatch.md`

```yaml
---
name: mt-unwatch
description: Stop watching a trader
---
```

Steps:
1. Ask for the user's Twitter handle if not known
2. Ask for the target trader's handle
3. Call `trader_unwatch` with both handles
4. Show confirmation

### 3d. Update mt-help and mt-status

Remove "coming soon" markers from `/mt-cancel`, `/mt-watch`, `/mt-unwatch`.
Update mt-status tool table to include the 3 new free tools.

### 3e. Update hooks/context.json

Add `trader_cancel_last`, `trader_watch`, `trader_unwatch` to the free tools list in the context injection.

### Phase 3 Acceptance Criteria

- [ ] 12 command files in `commands/` directory
- [ ] mt-help shows all 12 commands with no "coming soon" markers
- [ ] mt-status lists all 9 MCP tools
- [ ] hooks/context.json lists all 9 tools
- [ ] All commands tested end-to-end against live server

---

## Phase 4 -- Skill Update

**Goal:** Update the `mangrove-trader` skill to reference all 12 commands.
**Dependencies:** Phase 3 complete.
**Delegate to:** `backend-developer`

### 4a. Update `skills/mangrove-trader/SKILL.md`

Changes needed:
1. Add sections for cancel, watch, unwatch with tool names and steps
2. Update the Tool Quick Reference table (9 tools total)
3. Add "Other Twitter Commands" section referencing mt-cancel, mt-watch, mt-unwatch
4. Update the description trigger words to include: cancel, watch, unwatch, follow, watchlist
5. Bump version to 2.0.0

### 4b. Update CLAUDE.md

Update the structure section and tool count:
- Tools: 9 total (6 existing + 3 new)
- Commands: 12 total

### 4c. Update plugin.json

Bump version to 2.0.0 in `.claude-plugin/plugin.json`.

### 4d. Update hooks/context.json

Final version with all 9 tools listed.

### Phase 4 Acceptance Criteria

- [ ] Skill SKILL.md documents all 12 commands and 9 tools
- [ ] CLAUDE.md reflects 9 tools and 12 commands
- [ ] plugin.json version bumped to 2.0.0
- [ ] All keyword triggers in skill description cover the full command set
- [ ] Context hook lists all 9 tools with correct pricing

---

## File Change Summary

### Phase 1 (plugin-side, 8 commands)

| Action | File |
|--------|------|
| DELETE | `commands/stats.md` |
| DELETE | `commands/status.md` |
| DELETE | `commands/track.md` |
| CREATE | `commands/mt-stats.md` |
| CREATE | `commands/mt-report.md` |
| CREATE | `commands/mt-last.md` |
| CREATE | `commands/mt-track.md` |
| CREATE | `commands/mt-status.md` |
| CREATE | `commands/mt-leaderboard.md` |
| CREATE | `commands/mt-search.md` |
| CREATE | `commands/mt-history.md` |
| CREATE | `commands/mt-help.md` |
| MODIFY | `hooks/context.json` |

### Phase 2 (MangroveTrader server, 3 new MCP tools)

| Action | File | Repo |
|--------|------|------|
| MODIFY | `src/mcp/tools_trader.py` | MangroveTrader |
| MODIFY | `src/mcp/registry.py` | MangroveTrader |
| CREATE | `tests/test_mcp_tools_cancel_watch.py` | MangroveTrader |

### Phase 3 (plugin-side, 3 final commands)

| Action | File |
|--------|------|
| CREATE | `commands/mt-cancel.md` |
| CREATE | `commands/mt-watch.md` |
| CREATE | `commands/mt-unwatch.md` |
| MODIFY | `commands/mt-help.md` |
| MODIFY | `commands/mt-status.md` |
| MODIFY | `hooks/context.json` |

### Phase 4 (skill + metadata updates)

| Action | File |
|--------|------|
| MODIFY | `skills/mangrove-trader/SKILL.md` |
| MODIFY | `CLAUDE.md` |
| MODIFY | `.claude-plugin/plugin.json` |
| MODIFY | `hooks/context.json` |

---

## Delegation Summary

| Phase | Subagent | Repo |
|-------|----------|------|
| 1 | `backend-developer` | mangrove-trader-plugin |
| 2 | `backend-developer` (via MangroveTrader product owner) | MangroveTrader |
| 3 | `backend-developer` | mangrove-trader-plugin |
| 4 | `backend-developer` | mangrove-trader-plugin |

---

## Risks and Notes

1. **Phase 2 is the bottleneck.** Plugin Phases 1 and 3 are trivial markdown file creation. Phase 2 requires server-side Python, tests, and deployment.
2. **Cancel window logic.** The Twitter handler uses Grok LLM for witty rejection messages when the cancel window expires. The MCP tool should return a plain structured error -- no LLM call.
3. **Identity for watch/unwatch/cancel.** The MCP tools require the caller to provide their own `twitter_handle`. There is no auth on free tools, so a user could theoretically cancel someone else's trade. This matches the Twitter model (anyone can tweet `cancel last` but it only applies to the tweet author). The MCP tool should behave the same -- `twitter_handle` identifies the trader.
4. **Backward compatibility.** Renaming commands from `/stats` to `/mt-stats` is a breaking change for any users who have muscle memory with the old names. Since the plugin is at v1.0.0 with minimal adoption, this is acceptable. Bump to v2.0.0 signals the break.
5. **No `.mcp.json` changes needed.** The server URL stays the same. New tools are automatically available once deployed server-side.
