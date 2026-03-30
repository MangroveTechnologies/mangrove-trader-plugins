---
name: mt-report
description: Detailed performance report -- return %, Sharpe ratio, max drawdown, scoring breakdown (free)
---

# mt-report

Get a detailed performance report for a trader.

## Steps

1. Use the handle from `/mt-set-handle` if set. Otherwise ask for Twitter handle.
2. Ask for timeframe if not specified. Valid: `daily`, `weekly`, `monthly`, `all_time`, `30d`, `7d`. Default: `all_time`
3. Call the `trader_performance_report` MCP tool with `twitter_handle` and `timeframe`
4. **If MCP tool is not available**, fall back to REST: `POST https://api.mangrovetraders.com/api/v1/trader/performance_report` with `{"twitter_handle": "<handle>", "timeframe": "<timeframe>"}`
5. Present results with scoring breakdown:
   - **Composite Score** and **Rank**
   - **Total Return %** (50% of score weight)
   - **Sharpe Ratio** -- consistency measure (30% of score weight)
   - **Max Drawdown %** -- risk management, lower is better (20% of score weight)
   - **Win Rate** and **Trade Count**
6. If all metrics are null, note that scoring runs at midnight UTC and the trader may not have enough closed trades yet

## Scoring Formula

| Component | Weight | Metric |
|-----------|--------|--------|
| Return | 50% | Total return percentage |
| Consistency | 30% | Sharpe ratio |
| Risk Management | 20% | Max drawdown (lower is better) |
