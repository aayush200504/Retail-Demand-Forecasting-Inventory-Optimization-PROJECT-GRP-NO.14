select
    store_id,
    item_id,
    wm_yr_wk,
    sell_price
from `phonic-chemist-509603-v9.m5_raw.sell_prices`
where sell_price > 0
