## Resolution (Day 11)
- Rewrote the weekly aggregation to avoid exploding the full item-level
  daily table: summed the wide `d_1...d_1913` columns directly by mapping
  each day to its week (`wm_yr_wk`) via the calendar, then reshaped only
  the already-aggregated (store x cat x dept x week) result — 19,180 rows
  instead of 58M.
- Loaded directly via `pandas.DataFrame -> BigQuery` (load_table_from_dataframe),
  bypassing the dbt model execution for this table.
- `mart_weekly_sales` is live in `m5_analytics` with 19,180 rows.
