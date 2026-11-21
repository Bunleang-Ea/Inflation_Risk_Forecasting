import pandas as pd
import streamlit as st

import api_client

# Page title for model training and evaluation results.
st.title("📈 Model")

# Allow the user to start a new training run.
with st.expander("Retrain the model"):
    st.write("Cleans the data, compares models with cross-validation, tunes the best one "
             "and evaluates it on the test set. Takes a few seconds to a few minutes.")
    if st.button("Train model", type="primary"):
        with st.spinner("Training model..."):
            try:
                # The backend handles cleaning, training, and saving the model.
                api_client.train()
                st.success("Model trained and saved.")
            except api_client.APIError as e:
                # Display backend errors without crashing the page.
                st.error(str(e))

# Load the saved metrics report from the backend.
try:
    report = api_client.get_metrics()
except api_client.APIError as e:
    if str(e).startswith("404"):
        # A 404 means the model has not been trained yet.
        st.info("No trained model yet. Open **Retrain the model** above.")
        st.stop()
    # Show all other API errors using the shared helper.
    api_client.show_error_and_stop(e)

# Show the selected model and training metadata.
st.subheader(f"Final model: {report['best_model']}")
st.caption(f"Task: {report['task_type']} · target `{report['target']}` · "
           f"trained {report['trained_at']} · {report['n_train']} train / {report['n_test']} test rows")
st.write("Best parameters:", report["best_params"] or "default")

# --- Test metrics -----------------------------------------------------------
# These values measure performance on unseen test data.
st.subheader("Performance on the test set")
cols = st.columns(len(report["test_metrics"]))
for col, (name, value) in zip(cols, report["test_metrics"].items()):
    col.metric(name.upper(), value)

# --- Model comparison -------------------------------------------------------
# Compare candidate models using cross-validation results.
st.subheader("Model comparison (cross-validation)")
metric = report["primary_metric"]
cv = pd.DataFrame(report["cv_results"])
st.dataframe(cv, width="stretch", hide_index=True)
comparison_value = f"cv_{metric}_mean"
comparison_chart_data = cv.set_index("model")[[comparison_value]]
comparison_chart_data.columns = [metric.replace("_", " ").title()]
st.caption("Chart labels — Y-axis: Model | X-axis: Cross-Validation Score")
st.bar_chart(comparison_chart_data, horizontal=True, height=300)

# --- Feature importance -----------------------------------------------------
# Display the most important input features when available.
if report.get("feature_importance"):
    st.subheader("Feature importance")
    importance = pd.Series(report["feature_importance"]).head(15)
    st.caption("Chart labels — Y-axis: Feature | X-axis: Importance Score")
    st.bar_chart(importance, horizontal=True, height=400)
