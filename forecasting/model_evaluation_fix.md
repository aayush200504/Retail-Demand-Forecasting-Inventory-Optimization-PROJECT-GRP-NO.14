# Model Evaluation

Holdout: last 12 weeks. Metric: WMAPE (lower is better).

| Model | Level | WMAPE |
|---|---|---|
| Prophet | FOODS | 11.2% |
| Prophet | HOUSEHOLD | 4.5% |
| Prophet | HOBBIES | 8.8% |
| LightGBM | Store x Dept | 10.3% |

Notes:
- LightGBM uses lags of 12 weeks or more, so the 4-week horizon needs no recursive forecasting.
- Safety stock = z x holdout error std x sqrt(4).
