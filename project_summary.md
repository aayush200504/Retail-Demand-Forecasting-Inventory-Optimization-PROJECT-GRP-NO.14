# Project Summary: Retail Demand Forecasting & Inventory Optimization

## Objective
Forecast weekly demand for Walmart M5 data and turn forecasts into inventory recommendations.

## Pipeline
1. Raw M5 CSVs loaded into BigQuery (m5_raw)
2. dbt staging models and schema tests (m5_analytics)
3. Weekly store x dept aggregation
4. Prophet (category level) and LightGBM (store x dept)
5. Forecasts stored in BigQuery (demand_forecasts)
6. Streamlit dashboard with what-if price scenarios and safety stock

## Results (12-week holdout, WMAPE)
- Prophet: FOODS 11.2%, HOUSEHOLD 4.5%, HOBBIES 8.8%
- LightGBM store x dept: 10.3%

## Key decisions
- Weekly aggregation instead of daily: the daily table (58M rows) exceeded the BigQuery Sandbox storage cap.
- LightGBM lags of 12 weeks or more, so the 4-week horizon needs no recursive forecasting.
- Safety stock = z x holdout error std x sqrt(4).

## Limitations
- Price elasticity in the what-if scenario is an assumed value, not estimated from data.
- Forecast horizon is 4 weeks.

## Future work
- Estimate elasticity from price history
- Add hierarchical reconciliation across levels
- Schedule retraining
