import pandas as pd
import streamlit as st

import api_client

# Page title for the prediction history view.
st.title("🕘 Prediction History")

# Retrieve the predictions stored by the backend or current session.
try:
    items = api_client.get_history()["items"]
except api_client.APIError as e:
    api_client.show_error_and_stop(e)

# Tell the user how to create the first history entry.
if not items:
    st.info("No predictions yet. Try the **Prediction** page.")
    st.stop()

# Flatten each prediction into one row for the table.
rows = [{"time": it["created_at"], "prediction": it["prediction"], **it["input"]} for it in items]
st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
