---
name: mt-report
description: Detailed performance report -- return %, Sharpe ratio, max drawdown, scoring breakdown (free)
---

# mt-report

Get a detailed performance report for a trader.

## Steps

1. Check the `MT_AUTH_TOKEN` environment variable. If set, use it as `auth_token` — do NOT ask for a Twitter handle.
2. If `MT_AUTH_TOKEN` is not set, call `trader_login` to get a verification URL and stop — do not fall back to asking for a handle.
3. Ask for timeframe if not specified. Valid: `daily`, `weekly`, `monthly`, `all_time`, `30d`, `7d`. Default: `all_time`
4. Call the `trader_performance_report` MCP tool with `auth_token` and `timeframe`.
5. **If MCP tool is not available**, fall back to REST: `POST https://api.mangrovetraders.com/api/v1/trader/performance_report` with `{"auth_token": "<token>", "timeframe": "<timeframe>"}`
6. Present results with scoring breakdown:
   - **Composite Score** and **Rank**
   - **Total Return %** (50% of score weight)
   - **Sharpe Ratio** -- consistency measure (30% of score weight)
   - **Max Drawdown %** -- risk management, lower is better (20% of score weight)
   - **Win Rate** and **Trade Count**
7. If all metrics are null, note that scoring runs at midnight UTC and the trader may not have enough closed trades yet

## Scoring Formula

| Component | Weight | Metric |
|-----------|--------|--------|
| Return | 50% | Total return percentage |
| Consistency | 30% | Sharpe ratio |
| Risk Management | 20% | Max drawdown (lower is better) |
