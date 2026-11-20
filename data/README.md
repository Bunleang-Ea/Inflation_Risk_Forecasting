# Data Dictionary & Documentation

```
data/
├── raw/         # Original dataset: data/raw/inflation_data.csv
└── processed/   # Clean data for modeling: data/processed/clean.csv
```

## Dataset: Inflation & Consumer Price Index (CPI) Dataset (2005 - 2025)

Monthly macroeconomic inflation metrics covering 21 years (January 2005 to December 2025; 252 monthly observations).

| Column | Type | Description | Unit / Range |
|---|---|---|---|
| `Date` | Date | Month and Year of macroeconomic reporting | YYYY-MM-DD (2005-01-01 to 2025-12-01) |
| `CPI_all_item` | Numeric | Headline Consumer Price Index for all items | Index (~87.98 to ~211.53) |
| `MoM_Change_CPI_all_item` | Numeric | Month-over-Month percentage change in CPI | % (-3.93% to +8.27%) |
| `YoY_Change_CPI_all_item` | Numeric | Year-over-Year percentage change (Annual Inflation Rate) | % (-5.68% to +35.57%) |
| `CPI_3_Month_Moving_Avg` | Numeric | 3-Month Moving Average of CPI index | Index |
| `CPI_12_Month_Moving_Avg`| Numeric | 12-Month Moving Average of CPI index (Annual trend) | Index |
| `YoY_3_Month_Avg` | Numeric | 3-Month Rolling Average of YoY inflation | % |
| `YoY_12_Month_Avg` | Numeric | 12-Month Rolling Average of YoY inflation | % |

## Inflation Risk Regimes

In macroeconomic policy and central banking, annual inflation is typically categorized as:
* **Low / Normal (Target Zone)**: YoY $\le 3.0\%$ (Price stability, steady economic conditions)
* **Moderate Risk**: $3.0\% < \text{YoY} \le 5.0\%$ (Emerging price pressures, monitoring required)
* **Elevated Risk**: $5.0\% < \text{YoY} \le 8.0\%$ (Monetary tightening considerations, notable cost-of-living impact)
* **High Risk / Crisis**: $\text{YoY} > 8.0\%$ (Severe inflationary shock, rapid purchasing power degradation)
