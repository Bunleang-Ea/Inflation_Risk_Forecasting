# Model Card

- **Trained:** 2026-11-20T20:26:46
- **Task:** regression – predict `YoY_Change_CPI_all_item`
- **Model:** Linear Regression
- **Best parameters:** {}
- **Data:** 201 training rows, 51 test rows
- **Selection metric:** neg_root_mean_squared_error (5-fold CV)

## Test-set performance

| Metric | Value |
|---|---|
| mae | 0.4375 |
| rmse | 0.6489 |
| r2 | 0.9804 |

## Model comparison (cross-validation)

| Model | neg_root_mean_squared_error (mean ± std) |
|---|---|
| Linear Regression | -0.6897 ± 0.0824 |
| Ridge | -0.6984 ± 0.1064 |
| Gradient Boosting | -0.973 ± 0.1495 |
| Random Forest | -1.1262 ± 0.3047 |

## Limitations

👉 TODO: who should NOT use this model, known biases, data limitations.
