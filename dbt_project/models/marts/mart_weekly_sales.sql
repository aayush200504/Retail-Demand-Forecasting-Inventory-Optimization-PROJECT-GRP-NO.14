select
    store_id,
    cat_id,
    dept_id,
    wm_yr_wk,
    min(date) as week_start,
    sum(units_sold) as total_units_sold,
    sum(revenue) as total_revenue,
    avg(sell_price) as avg_sell_price
from {{ ref('mart_daily_sales') }}
group by store_id, cat_id, dept_id, wm_yr_wk
