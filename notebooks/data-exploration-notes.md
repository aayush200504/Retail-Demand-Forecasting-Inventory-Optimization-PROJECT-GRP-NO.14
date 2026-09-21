# M5 Dataset — Exploration Notes (Day 2)

## Dataset Shapes
- `sales_train_validation.csv`: 30,490 rows × 1,919 columns (item-level daily sales, 1,913 days of history)
- `calendar.csv`: 1,969 rows × 14 columns (date-to-day mapping, events, SNAP flags)
- `sell_prices.csv`: 6,841,121 rows × 4 columns (weekly price per item per store)

## Schema Summary

| File | Grain | Key Columns |
|---|---|---|
| sales_train_validation.csv | item x store x day | item_id, dept_id, cat_id, store_id, state_id, d_1...d_1913 |
| calendar.csv | day | date, wm_yr_wk, event_name_1, snap_CA/TX/WI |
| sell_prices.csv | item x store x week | store_id, item_id, wm_yr_wk, sell_price |

## Categories Found
- HOBBIES, HOUSEHOLD, FOODS (cat_id)
- 10 stores across CA, TX, WI (store_id)

## Next Steps
- Reshape sales data from wide (d_1...d_1913) to long format for time-series modeling
- Join calendar and price data to sales for feature engineering
- Load into BigQuery for the ETL pipeline (Day 3-4)
