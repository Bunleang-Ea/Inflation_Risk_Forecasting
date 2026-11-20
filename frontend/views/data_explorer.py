import streamlit as st
import pandas as pd
import numpy as np
import api_client

# Page title and short description.
st.title("📊 Data Explorer – Macroeconomic CPI Analysis")
st.markdown("Explore historical price indices, annual inflation dynamics, volatility regimes, and moving averages from 2005 to 2025.")

# Load the cleaned dataset through the API client.
df = api_client.get_raw_dataframe()

# Stop early when no data is available.
if df.empty:
    st.error("No dataset found.")
    st.stop()

# Convert dates and keep records in chronological order.
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# Create date limits for the two date selectors.
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

f1, f2 = st.columns([2, 2])
with f1:
    start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
with f2:
    end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Keep only rows inside the selected date range.
mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
filtered_df = df.loc[mask].copy()

# Stop if the selected dates contain no observations.
if filtered_df.empty:
    st.warning("No data points found for the selected date range.")
    st.stop()

# Calculate summary values for the selected period.
st.caption(f"Displaying **{len(filtered_df)} monthly observations** from {start_date} to {end_date}")

m1, m2, m3, m4 = st.columns(4)
avg_cpi = filtered_df["CPI_all_item"].mean()
avg_yoy = filtered_df["YoY_Change_CPI_all_item"].mean()
max_yoy = filtered_df["YoY_Change_CPI_all_item"].max()
min_yoy = filtered_df["YoY_Change_CPI_all_item"].min()

m1.metric("Average CPI Index", f"{avg_cpi:.2f}")
m2.metric("Mean Annual Inflation (YoY)", f"{avg_yoy:.2f}%")
m3.metric("Peak Annual Inflation", f"{max_yoy:.2f}%")
m4.metric("Lowest Annual Inflation", f"{min_yoy:.2f}%")

# Create separate tabs for the main analysis views.
st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Price Index & Moving Averages",
    "⚡ YoY & MoM Inflation Trajectory",
    "📊 Volatility & Distributions",
    "📋 Data Table & Export",
])

# Tab 1: compare CPI with short- and long-term moving averages.
with tab1:
    st.subheader("Headline CPI Index & Trend Smoothing")
    st.markdown(
        "Compare raw Consumer Price Index with short-term (3-month) and long-term (12-month) moving averages "
        "to identify macroeconomic momentum shifts and trend reversals."
    )
    chart_data = filtered_df.set_index("Date")[["CPI_all_item", "CPI_3_Month_Moving_Avg", "CPI_12_Month_Moving_Avg"]]
    chart_data.columns = ["CPI All Items", "3-Month Moving Avg", "12-Month Moving Avg"]
    st.line_chart(chart_data, height=400)

    # A positive spread means recent CPI is above the long-term trend.
    filtered_df["Momentum_Spread"] = filtered_df["CPI_3_Month_Moving_Avg"] - filtered_df["CPI_12_Month_Moving_Avg"]
    latest_spread = filtered_df.iloc[-1]["Momentum_Spread"]
    if latest_spread > 0:
        st.success(f"🟢 **Upward Price Momentum**: 3-Month Moving Average is currently **+{latest_spread:.2f} pts** above the 12-Month trend.")
    else:
        st.info(f"🔵 **Disinflationary Momentum**: 3-Month Moving Average is currently **{latest_spread:.2f} pts** below the 12-Month trend.")

# Tab 2: display annual inflation trends and monthly price changes.
with tab2:
    st.subheader("Annual (YoY) Inflation & Monthly (MoM) Volatility")
    st.markdown("Annual inflation reflects macroeconomic purchasing power loss, while MoM shows monthly pricing pressure shocks.")

    yoy_chart = filtered_df.set_index("Date")[["YoY_Change_CPI_all_item", "YoY_3_Month_Avg", "YoY_12_Month_Avg"]]
    yoy_chart.columns = ["YoY Inflation Rate (%)", "YoY 3-Month Average", "YoY 12-Month Average"]
    st.line_chart(yoy_chart, height=350)

    st.markdown("##### **Monthly Price Changes (MoM %)**")
    mom_chart = filtered_df.set_index("Date")["MoM_Change_CPI_all_item"]
    st.bar_chart(mom_chart, height=220)

# Tab 3: show the distribution and descriptive statistics of inflation.
with tab3:
    st.subheader("Distribution Analysis & Statistical Dispersion")
    c_left, c_right = st.columns([1, 1])

    with c_left:
        st.markdown("**YoY Inflation Rate Histogram**")
        yoy_values = filtered_df["YoY_Change_CPI_all_item"]
        hist_counts, hist_bins = np.histogram(yoy_values, bins=15)
        hist_df = pd.DataFrame({
            "Inflation Range (%)": [f"{hist_bins[i]:.1f} to {hist_bins[i+1]:.1f}" for i in range(len(hist_counts))],
            "Frequency (Months)": hist_counts
        })
        st.bar_chart(hist_df.set_index("Inflation Range (%)"), height=300)

    with c_right:
        st.markdown("**Summary Statistics for Selected Window**")
        stats_cols = [
            "CPI_all_item",
            "MoM_Change_CPI_all_item",
            "YoY_Change_CPI_all_item",
            "CPI_3_Month_Moving_Avg",
            "CPI_12_Month_Moving_Avg",
            "YoY_12_Month_Avg",
        ]
        stats = filtered_df[stats_cols].describe().T[["mean", "std", "min", "25%", "50%", "75%", "max"]]
        stats.columns = ["Mean", "Std Dev", "Min", "25%", "Median", "75%", "Max"]
        st.dataframe(stats.round(2), use_container_width=True)

# Tab 4: show the filtered records and allow CSV export.
with tab4:
    st.subheader("Dataset Records & Feature Dictionary")

    # Explain the meaning of each dataset column.
    with st.expander("📖 Feature Definitions (Column Data Dictionary)", expanded=True):
        st.markdown(
            """
| Column / Feature | Unit / Type | Short Definition |
|---|---|---|
| `Date` | Date (YYYY-MM-DD) | Monthly reporting timestamp for the macroeconomic observation. |
| `CPI_all_item` | Index Number | **Headline CPI**: The weighted price level of all consumer goods and services in the basket. |
| `MoM_Change_CPI_all_item` | Percentage (%) | **Month-over-Month Change**: Short-term monthly price movement velocity compared to the previous month. |
| `YoY_Change_CPI_all_item` | Percentage (%) | **Year-over-Year Inflation**: Official annual inflation rate compared to the same month in the previous year. |
| `CPI_3_Month_Moving_Avg` | Index Number | **3-Month CPI Average**: Short-term rolling mean of CPI level to track quarterly momentum. |
| `CPI_12_Month_Moving_Avg`| Index Number | **12-Month CPI Average**: Annual rolling mean of CPI level representing the smoothed long-term price trend. |
| `YoY_3_Month_Avg` | Percentage (%) | **3-Month YoY Average**: Rolling average of annual inflation rate, smoothing single-month volatility. |
| `YoY_12_Month_Avg` | Percentage (%) | **12-Month YoY Average**: Annual average inflation rate representing the medium-term core baseline. |
"""
        )

    st.markdown("##### **Filtered Observation Records**")
    display_df = filtered_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name=f"cpi_inflation_{start_date}_to_{end_date}.csv",
        mime="text/csv",
    )
