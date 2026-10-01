# Day 10 — Known Issue: BigQuery Sandbox Storage Quota

## What happened
- Built `mart_daily_sales.sql` and `mart_weekly_sales.sql` as dbt models joining staging tables (calendar, sell_prices, sales_unpivoted)
- `mart_daily_sales` ran successfully once (58.3M rows, 687MB processed) but then subsequent runs failed with:
  `Quota exceeded: Your project exceeded quota for free storage for projects`
- Root cause: BigQuery Sandbox (no billing account linked) has a hard free storage cap, and the daily-grain table (item x store x day ≈ 58M rows) exceeds it

## Status
- Blocked until billing is linked to the GCP project (covered by $300 trial credit, no charge expected) — flagged to manager for decision
- Workaround in progress: building the weekly aggregate directly in Pandas (Colab) and loading only the small result table into BigQuery, bypassing the need to materialize the full daily-grain table

## Next steps
- Get manager decision on linking billing vs. staying on the Pandas workaround
- Once resolved, re-run `dbt run --select marts` for both models
