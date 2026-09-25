# EDA Findings — Week 1

## Overall Sales Trend
- Total units sold shows a gradual upward trend from day 1 to ~day 1913
- Strong weekly seasonality (repeating peaks/dips)
- 5 sharp drops to near-zero sales — correspond to Christmas Day store closures each year (2011-2015)

## Sales by Category (snapshot: day 1900)
| Category | Units Sold |
|---|---|
| FOODS | ~29,000 |
| HOUSEHOLD | ~10,000 |
| HOBBIES | ~4,000 |

FOODS is by far the dominant category — forecasting accuracy here matters most for business impact.

## Sales by Store (snapshot: day 1900)
- Top performers: **CA_3**, **WI_2**
- Lowest performer: **CA_4**
- Store-level variation suggests forecasting should be done per-store, not globally

## Calendar Structure
- `wday` 1–7 maps Saturday → Friday (M5 convention)
- Evenly distributed ~281–282 occurrences of each weekday across the dataset (2011-01-29 to 2016-06-19)

## Implications for Modeling (Week 3)
- Need per-store, per-category (or per-item) forecasting rather than one global model
- Must handle known zero-sales days (holidays) as a feature, not noise
- FOODS category should be prioritized/validated most carefully given its volume share
