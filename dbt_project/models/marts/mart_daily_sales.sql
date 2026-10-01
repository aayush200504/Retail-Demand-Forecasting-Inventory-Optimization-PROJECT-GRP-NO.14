select
    s.id,
    s.item_id,
    s.dept_id,
    s.cat_id,
    s.store_id,
    s.state_id,
    c.date,
    c.wm_yr_wk,
    c.wday,
    c.weekday,
    c.month,
    c.year,
    c.event_name_1,
    c.event_type_1,
    c.snap_CA,
    c.snap_TX,
    c.snap_WI,
    p.sell_price,
    s.units_sold,
    s.units_sold * p.sell_price as revenue
from {{ ref('stg_sales_unpivoted') }} s
inner join {{ ref('stg_calendar') }} c
    on s.day_num = c.day_num
left join {{ ref('stg_sell_prices') }} p
    on s.store_id = p.store_id
    and s.item_id = p.item_id
    and c.wm_yr_wk = p.wm_yr_wk
