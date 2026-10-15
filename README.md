# Retail Demand Forecasting & Inventory Optimization

Time-series forecasting platform that predicts weekly product demand per store and department from the M5 (Walmart) dataset and turns the forecasts into inventory recommendations.

**Live dashboard:** [_Streamlit_Website_Overview_Cloud_](https://retail-demand-forecasting-inventory-optimization-project-grp-14.streamlit.app/)

## Tech stack
Python, SQL, Google BigQuery (data warehouse), dbt (transformations), Prophet and LightGBM (forecasting), Streamlit (dashboard), Docker.

## Architecture
```
M5 CSVs -> BigQuery (m5_raw) -> dbt staging models -> weekly mart (m5_analytics)
        -> Prophet / LightGBM forecasting -> forecasts in BigQuery + CSV
        -> Streamlit dashboard (forecast, what-if price scenario, inventory recommendation)
```

## What was built
| Stage | Work | Location |
|---|---|---|
| Data warehouse | Loaded raw M5 sales, calendar and prices into BigQuery; ran null, price and date-range checks | `notebooks/` |
| EDA | Sales trend, category and store breakdown, weekday and holiday patterns | `notebooks/eda-notes.md` |
| dbt | Staging models for calendar, prices and unpivoted sales, with schema tests | `dbt_project/` |
| Weekly mart | Units per store, category, department and week (19,180 rows) | BigQuery `m5_analytics.mart_weekly_sales` |
| Prophet | Category-level weekly forecasts with 12-week holdout | `forecasting/` |
| LightGBM | Store x department forecasts using lag, rolling, event and SNAP features, tuned on a validation window | `forecasting/` |
| Evaluation | Prophet vs LightGBM comparison (MAE, RMSE, WMAPE, bias) | `forecasting/model_evaluation.md` |
| Forecast storage | 4-week forecast per store and department written to BigQuery and CSV | `forecasting/forecasts.csv` |
| Dashboard | Store and category filters, 30-day forecast, what-if price slider, inventory recommendation | `dashboard/app.py` |

## Results (12-week holdout)
| Model | Level | WMAPE |
|---|---|---|
| Prophet | FOODS | 11.2% |
| Prophet | HOUSEHOLD | 4.5% |
| Prophet | HOBBIES | 8.8% |
| LightGBM | Store x department | 10.3% |

LightGBM is evaluated at a finer grain than Prophet, so the numbers are not directly comparable. See `forecasting/model_evaluation.md` for the same-level comparison.

## Inventory recommendation logic
Recommended stock for the next 4 weeks = forecast units (with the what-if price effect) + safety stock, where safety stock = service-level z-score x holdout error standard deviation x sqrt(4 weeks). The price effect uses an assumed elasticity set in the sidebar (default -1.2); it is a scenario input, not an estimated value.

## Run locally
```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## Run with Docker
```bash
docker build -t retail-forecast .
docker run -p 8501:8501 retail-forecast
```
Open http://localhost:8501

## Known limitations
- BigQuery Sandbox (no billing) has a free storage cap. Materializing the full item x store x day table (58M rows) exceeded it, so forecasting runs at weekly store x department grain.
- Forecast horizon is 4 weeks. All lag features are 12 weeks or more, so no recursive forecasting is needed.
- Price what-if uses an assumed elasticity rather than one estimated from the price data.

## Repository layout
```
dashboard/      Streamlit app
dbt_project/    dbt models and tests
forecasting/    Prophet and LightGBM notebooks, forecasts, evaluation
notebooks/      Data loading, quality checks, EDA
```
