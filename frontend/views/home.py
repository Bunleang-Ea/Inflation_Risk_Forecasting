import streamlit as st
import pandas as pd
import api_client
import config

# Display the project identity and description.
st.title(f"{config.PROJECT_ICON} {config.PROJECT_TITLE}")
st.markdown(f"*{config.PROJECT_DESCRIPTION}*")

# Load the dataset used for the dashboard indicators.
df = api_client.get_raw_dataframe()

# Stop when the data source is unavailable.
if df.empty:
    st.error("No dataset found. Please ensure the CSV is placed in data/raw/ or frontend/data/.")
    st.stop()

# Sort records so the latest and previous observations are correct.
df = df.sort_values("Date").reset_index(drop=True)
latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) > 1 else latest

# Show the latest macroeconomic values and their change from the previous month.
st.divider()

st.subheader("📌 Latest Macroeconomic Indicators (Dec 2025)")

k1, k2, k3, k4, k5 = st.columns(5)

# Read the values used by the KPI cards.
cpi_val = latest["CPI_all_item"]
cpi_prev = prev["CPI_all_item"]
yoy_val = latest["YoY_Change_CPI_all_item"]
yoy_prev = prev["YoY_Change_CPI_all_item"]
mom_val = latest["MoM_Change_CPI_all_item"]
mom_prev = prev["MoM_Change_CPI_all_item"]
ma12_val = latest["YoY_12_Month_Avg"]

k1.metric(
    "CPI All Items",
    f"{cpi_val:.2f}",
    delta=f"{cpi_val - cpi_prev:+.2f} pts",
    help="1. CPI All Items: Headline Consumer Price Index tracking the price level of a representative basket of goods and services.",
)
k2.metric(
    "YoY Inflation",
    f"{yoy_val:.2f}%",
    delta=f"{yoy_val - yoy_prev:+.2f}% YoY",
    help="2. YoY Inflation: Year-over-Year annual percentage price change compared to the exact same month last year.",
)
k3.metric(
    "MoM Price Change",
    f"{mom_val:.2f}%",
    delta=f"{mom_val - mom_prev:+.2f}% MoM",
    help="3. MoM Price Change: Month-over-Month percentage change indicating immediate monthly pricing velocity.",
)
k4.metric(
    "12M Core Average",
    f"{ma12_val:.2f}%",
    delta=f"{ma12_val - prev['YoY_12_Month_Avg']:+.2f}% YoY",
    help="4. 12M Core Average: 12-Month rolling average of YoY inflation to filter out seasonal and short-term volatility.",
)

# Assign a risk category using the annual inflation thresholds.
if yoy_val <= 3.0:
    regime_val = "🟢 Stable"
    regime_delta = "Low Risk (≤3%)"
    regime_help = "5. Inflation Regime: Annual inflation is within the central bank target stability zone (<= 3.0%)."
elif yoy_val <= 5.0:
    regime_val = "🟡 Moderate"
    regime_delta = "Watchlist (3-5%)"
    regime_help = "5. Inflation Regime: Moderate upward price pressures (3.0% - 5.0%)."
elif yoy_val <= 8.0:
    regime_val = "🟠 Elevated"
    regime_delta = "Warning (5-8%)"
    regime_help = "5. Inflation Regime: Significant cost of living escalation requiring policy monitoring (5.0% - 8.0%)."
else:
    regime_val = "🔴 Critical"
    regime_delta = "Shock (>8%)"
    regime_help = "5. Inflation Regime: Severe inflationary crisis (> 8.0%)."

k5.metric(
    "Inflation Regime",
    regime_val,
    delta=regime_delta,
    delta_color="off",
    help=regime_help,
)

# Explain the economic meaning and formulas behind the indicators.
with st.expander("📖 Indicator Definitions & Economic Methodology", expanded=True):
    st.markdown("Detailed breakdown of the macroeconomic metrics used throughout this forecasting platform:")

    d1, d2 = st.columns(2)

    with d1:
        st.markdown(
            """
            #### **1. CPI All Items (Consumer Price Index)**
            * **What it is:** A comprehensive index measuring the weighted average price level of a standardized basket of consumer goods and services (food, housing, utilities, transportation, health, and education).
            * **Economic Role:** Serves as the nominal price level benchmark. As CPI rises over time, purchasing power declines.

            #### **2. YoY Inflation (Year-over-Year % Change)**
            * **Formula:** $\\text{YoY}_t = \\frac{\\text{CPI}_t - \\text{CPI}_{t-12}}{\\text{CPI}_{t-12}} \\times 100\\%$
            * **What it is:** The official headline annual inflation rate comparing current price levels with the exact same month in the preceding year.
            * **Economic Role:** Key target for central banks (standard stability target is $\\le 3.0\\%$).

            #### **3. MoM Price Change (Month-over-Month % Change)**
            * **Formula:** $\\text{MoM}_t = \\frac{\\text{CPI}_t - \\text{CPI}_{t-1}}{\\text{CPI}_{t-1}} \\times 100\\%$
            * **What it is:** The monthly rate of price acceleration or deceleration.
            * **Economic Role:** Detects immediate short-term supply chain shocks or seasonal price spikes before they fully register in annual YoY numbers.
            """
        )

    with d2:
        st.markdown(
            """
            #### **4. 12M Core Average (12-Month Rolling Mean)**
            * **Formula:** $\\text{12M Avg}_t = \\frac{1}{12} \\sum_{i=0}^{11} \\text{YoY}_{t-i}$
            * **What it is:** The smoothed moving average of annual inflation over the past 12 months.
            * **Economic Role:** Filters out transient monthly noise, temporary harvest swings, and oil shocks to reveal the medium-term underlying inflation trend.

            #### **5. Inflation Regime (Risk Threshold Classification)**
            * **What it is:** A policy-driven macroeconomic risk category indicating price stability health:
              * 🟢 **Low / Stable ($\le 3.0\%$)**: Price stability corridor supporting sustainable growth and stable purchasing power.
              * 🟡 **Moderate Watchlist ($3.0\% - 5.0\%$)**: Emerging price pressures; requires close surveillance.
              * 🟠 **Elevated Risk ($5.0\% - 8.0\%$)**: Notable cost-of-living impact; signals potential monetary tightening.
              * 🔴 **Critical Shock ($> 8.0\%$)**: High inflation crisis (e.g. 2008 global commodity shock at 35.57%).
            """
        )

st.divider()

# Plot the long-term CPI trend and its 12-month moving average.
st.subheader("📈 Long-Term Trend Overview (2005 – 2025)")

st.markdown("**CPI All Items & 12-Month Moving Average**")
chart_df = df.set_index("Date")[["CPI_all_item", "CPI_12_Month_Moving_Avg"]]
chart_df.columns = ["Headline CPI", "12-Month Moving Average"]
st.line_chart(chart_df, height=320)

st.divider()

# Briefly explain what users can find on the main pages.
st.subheader("🛠️ Web App Structure")
g1, g2, g3 = st.columns(3)

with g1:
    st.markdown("#### 📊 **1. Data Explorer**")
    st.write(
        "Filter 21 years of monthly CPI data, inspect time-series trajectories, "
        "moving average crossovers, volatility distributions, and export data."
    )

with g2:
    st.markdown("#### 🔮 **2. Prediction**")
    st.write(
        "Input macroeconomic indicators or use the latest recorded values "
        "to forecast future YoY inflation rates and evaluate inflation risk."
    )

with g3:
    st.markdown("#### 📈 **3. Model Roadmap & About**")
    st.write(
        "Review CRISP-DM methodology, planned ML architectures (Random Forest, "
        "Gradient Boosting, ARIMA), evaluation targets, and team contributions."
    )
