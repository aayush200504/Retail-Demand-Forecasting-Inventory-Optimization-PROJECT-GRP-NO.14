"""
Retail Demand Forecasting & Inventory Optimization - Streamlit dashboard.
Reads forecasts.csv and weekly_history.csv (exported from BigQuery by forecast_storage.ipynb).
Run: streamlit run dashboard/app.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Retail Demand Forecasting", layout="wide")


@st.cache_data
def load_data():
    here = Path(__file__).resolve().parent
    for base in [here.parent / "forecasting", here, Path("forecasting"), Path(".")]:
        f, h = base / "forecasts.csv", base / "weekly_history.csv"
        if f.exists() and h.exists():
            fc = pd.read_csv(f, parse_dates=["week_start"])
            hist = pd.read_csv(h, parse_dates=["week_start"])
            return fc, hist
    st.error("forecasts.csv / weekly_history.csv not found. Put them in the forecasting/ folder.")
    st.stop()


fc, hist = load_data()

# ---------------- Sidebar filters ----------------
st.sidebar.header("Filters")
stores = ["All stores"] + sorted(fc["store_id"].unique())
store = st.sidebar.selectbox("Store", stores)
cats = ["All categories"] + sorted(fc["cat_id"].unique())
cat = st.sidebar.selectbox("Category", cats)

mask_fc = pd.Series(True, index=fc.index)
mask_h = pd.Series(True, index=hist.index)
if store != "All stores":
    mask_fc &= fc["store_id"] == store
    mask_h &= hist["store_id"] == store
if cat != "All categories":
    mask_fc &= fc["cat_id"] == cat
    mask_h &= hist["cat_id"] == cat
fc_f, hist_f = fc[mask_fc], hist[mask_h]

st.sidebar.header("What-if scenario")
price_change = st.sidebar.slider("Price change (%)", -30, 30, 0, step=1)
elasticity = st.sidebar.slider("Assumed price elasticity", -3.0, -0.2, -1.2, step=0.1,
                               help="Assumption: % change in units per 1% change in price.")
safety_z = st.sidebar.slider("Service level (z-score)", 1.0, 2.5, 1.65, step=0.05,
                             help="1.65 is roughly a 95% service level.")

# Price effect: units scale with (1 + price change) ** elasticity
factor = (1 + price_change / 100) ** elasticity

# ---------------- Aggregate by week ----------------
future = fc_f[fc_f["type"] == "future"].groupby("week_start", as_index=False)["forecast"].sum()
holdout = fc_f[fc_f["type"] == "holdout"].groupby("week_start", as_index=False)[["actual", "forecast"]].sum()
hist_w = hist_f.groupby("week_start", as_index=False)["units"].sum()
future["scenario"] = future["forecast"] * factor

# ---------------- KPIs ----------------
last4 = hist_w.sort_values("week_start").tail(4)["units"].sum()
next4 = future["forecast"].sum()
next4_s = future["scenario"].sum()
wmape = (np.abs(holdout["actual"] - holdout["forecast"]).sum() / holdout["actual"].sum()) if len(holdout) else np.nan

st.title("Retail Demand Forecasting & Inventory Optimization")
st.caption("M5 Walmart data | LightGBM weekly forecasts | 30-day (4-week) horizon")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Last 4 weeks (actual units)", f"{last4:,.0f}")
c2.metric("Next 4 weeks (forecast)", f"{next4:,.0f}", f"{(next4 / last4 - 1):+.1%} vs last 4 weeks")
c3.metric("Next 4 weeks (what-if)", f"{next4_s:,.0f}", f"{(next4_s / next4 - 1):+.1%} vs baseline")
c4.metric("Holdout WMAPE (12 weeks)", f"{wmape:.1%}" if not np.isnan(wmape) else "n/a")

# ---------------- Chart ----------------
fig = go.Figure()
recent = hist_w.sort_values("week_start").tail(52)
fig.add_trace(go.Scatter(x=recent["week_start"], y=recent["units"], name="Actual", mode="lines"))
fig.add_trace(go.Scatter(x=holdout["week_start"], y=holdout["forecast"], name="Model (holdout)",
                         mode="lines", line=dict(dash="dot")))
fig.add_trace(go.Scatter(x=future["week_start"], y=future["forecast"], name="Forecast (next 4 weeks)",
                         mode="lines+markers"))
if price_change != 0:
    fig.add_trace(go.Scatter(x=future["week_start"], y=future["scenario"],
                             name=f"What-if ({price_change:+d}% price)", mode="lines+markers",
                             line=dict(dash="dash")))
fig.update_layout(height=420, margin=dict(l=10, r=10, t=30, b=10), yaxis_title="Units per week",
                  legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, width="stretch")

# ---------------- Inventory recommendation ----------------
st.subheader("Inventory recommendation (next 4 weeks)")
err = fc_f[fc_f["type"] == "holdout"].copy()
err["abs_err"] = (err["actual"] - err["forecast"]).abs()
sigma = err.groupby(["store_id", "dept_id"])["abs_err"].std().rename("error_std")
rec = (fc_f[fc_f["type"] == "future"].groupby(["store_id", "cat_id", "dept_id"])["forecast"].sum()
       .rename("forecast_units").reset_index().merge(sigma.reset_index(), on=["store_id", "dept_id"], how="left"))
rec["error_std"] = rec["error_std"].fillna(0)
rec["scenario_units"] = rec["forecast_units"] * factor
rec["safety_stock"] = safety_z * rec["error_std"] * np.sqrt(4)
rec["recommended_stock"] = rec["scenario_units"] + rec["safety_stock"]
show = rec[["store_id", "cat_id", "dept_id", "forecast_units", "scenario_units", "safety_stock", "recommended_stock"]]
st.dataframe(show.round(0).sort_values("recommended_stock", ascending=False), width="stretch", hide_index=True)
st.caption("Recommended stock = what-if forecast for 4 weeks + safety stock (service-level z x holdout error std x sqrt(4 weeks)). "
           "Price effect uses the elasticity assumption in the sidebar, not an estimated value.")

st.download_button("Download recommendation CSV", show.round(0).to_csv(index=False), "inventory_recommendation.csv")
