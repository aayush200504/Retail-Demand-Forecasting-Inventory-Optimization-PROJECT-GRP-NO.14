-- Built via Pandas workaround (see docs/day10-known-issue.md) due to BigQuery
-- Sandbox storage quota. Logic: sum daily units per store/cat/dept into
-- weekly buckets using wm_yr_wk from the calendar, avoiding a full
-- item-level daily unpivot (58M+ rows) that exceeded free quota.
-- Loaded directly via pandas -> BigQuery, not via `dbt run`.

select
    store_id,
    cat_id,
    dept_id,
    wm_yr_wk,
    total_units_sold
from `phonic-chemist-509603-v9.m5_analytics.mart_weekly_sales`
