import streamlit as st
import config

# Show the project title and its main purpose.
st.title("ℹ️ About the Project")
st.markdown("Macroeconomic forecasting and risk intelligence system developed for DSE Web App Development for Data Science.")

# Split the page between project information and team details.
col1, col2 = st.columns([3, 2])

with col1:
    # Display the project's scope and objectives.
    st.subheader("🎯 Project Purpose & Scope")
    st.write(f"**{config.PROJECT_TITLE}**")
    st.write(config.PROJECT_DESCRIPTION)

    st.markdown(
        """
        - **Target Problem**: Inflation spikes cause rapid purchasing power erosion, supply chain uncertainty, and policy volatility.
        - **Target Users**: Economic analysts, business planners, financial institutions, and policy researchers.
        - **Core Value**: Early detection of price momentum acceleration through moving-average convergence/divergence and regression forecasting.
        """
    )

with col2:
    # Read the class and team names from the shared configuration.
    st.subheader("👥 Project Team")
    st.write(f"Class: **{config.CLASS_NAME}**")
    for member in config.TEAM_MEMBERS:
        st.markdown(f"- {member}")

# Describe the dataset columns used by the application.
st.divider()

st.subheader("📊 Dataset & Variable Dictionary")
st.write(config.DATA_SOURCE)

st.markdown(
    """
| Column Name | Metric Type | Description |
|---|---|---|
| `Date` | Timestamp | Monthly frequency from January 2005 to December 2025 (252 monthly records) |
| `CPI_all_item` | Index Level | Consumer Price Index for all goods and services basket |
| `MoM_Change_CPI_all_item` | Percentage (%) | Month-over-Month percentage change ($[CPI_t - CPI_{t-1}] / CPI_{t-1} \\times 100$) |
| `YoY_Change_CPI_all_item` | Percentage (%) | Year-over-Year annual inflation rate ($[CPI_t - CPI_{t-12}] / CPI_{t-12} \\times 100$) |
| `CPI_3_Month_Moving_Avg` | Moving Average | 3-Month rolling mean of CPI level (short-term momentum filter) |
| `CPI_12_Month_Moving_Avg`| Moving Average | 12-Month rolling mean of CPI level (annual baseline trend) |
| `YoY_3_Month_Avg` | Rolling Mean (%)| 3-Month average of annual inflation (smoothes single-month noise) |
| `YoY_12_Month_Avg` | Rolling Mean (%)| 12-Month average of annual inflation (core medium-term inflation anchor) |
"""
)

# Explain how the frontend, API, data, and ML layers work together.
st.divider()

st.subheader("🏗️ System Architecture & Technology Stack")
st.markdown(
    """
```
┌─────────────────────────────────┐        HTTP / JSON        ┌──────────────────────────────────┐
│       Streamlit Frontend        │ ────────────────────────▶ │   Backend REST API (FastAPI)     │
│   (app.py & modular views)      │ ◀──────────────────────── │      (Endpoints & Data Layer)    │
└─────────────────────────────────┘                           └──────────────────────────────────┘
                 │                                                              │
                 │ (Data / Ingestion Engine)                                    │ (Model Inference Service)
                 ▼                                                              ▼
┌─────────────────────────────────┐                           ┌──────────────────────────────────┐
│   Local Ingestion & Simulator   │                           │     Machine Learning Engine      │
│  (data/raw/inflation_data.csv)  │                           │   (scikit-learn Pipeline / CV)   │
└─────────────────────────────────┘                           └──────────────────────────────────┘
```

- **Frontend**: Streamlit 1.50+ (Multi-page architecture, responsive charts, KPI widgets)
- **Data Manipulation**: Pandas 2.0+ & NumPy
- **Planned Backend**: FastAPI (high-performance asynchronous Python REST API)
- **ML Framework**: scikit-learn (Ridge, Random Forest Regressor, Gradient Boosting)
- **Methodology**: CRISP-DM (Data Understanding, Preparation, Modeling, Evaluation, Deployment)
"""
)
