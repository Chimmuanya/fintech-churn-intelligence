"""
Streamlit dashboard skeleton for Fintech Churn Intelligence.

To run:
    pip install -r requirements.txt
    streamlit run dashboard/app.py

This app expects results/charts/cohort_matrix.csv produced by the notebook.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# page layout
st.set_page_config(page_title="Churn Intelligence", layout="wide")

# Title / Header
st.title("Fintech Churn Intelligence — Cohorts & Retention")

# Sidebar filters
st.sidebar.header("Filters & Options")
# In a full project you'd populate segments dynamically; for now static choices are fine
segment_choice = st.sidebar.selectbox("Segment", ["All", "high", "medium", "low"])
num_cohorts = st.sidebar.slider("Number of cohorts to show", min_value=3, max_value=12, value=6)

# load the cohort matrix CSV created by the notebook
try:
    cohort_matrix = pd.read_csv("results/charts/cohort_matrix.csv", index_col=0)
    # convert index back to datetime if it was saved as string
    try:
        cohort_matrix.index = pd.to_datetime(cohort_matrix.index)
    except Exception:
        # If parse fails, leave as-is
        pass
except FileNotFoundError:
    st.error("Cohort matrix not found. Run notebooks/01_eda_cohorts.ipynb first to produce results/charts/cohort_matrix.csv")
    st.stop()

st.markdown("### Retention curves (cohort-based)")
# build a simple line plot using matplotlib and seaborn
fig, ax = plt.subplots(figsize=(10, 5))

# show only the last `num_cohorts` cohorts (or first depending on how you want to order)
# Here, we pick the most recent cohorts by index ordering
cohorts_to_plot = cohort_matrix.index[-num_cohorts:]

for cohort in cohorts_to_plot:
    # get retention values as a list
    try:
        retention_values = cohort_matrix.loc[str(cohort)].values
    except KeyError:
        # sometimes the index types differ; use label matching
        retention_values = cohort_matrix.loc[cohort].values
    months = list(range(len(retention_values)))
    ax.plot(months, retention_values, marker='o', label=str(pd.to_datetime(cohort).date()))

ax.set_xlabel("Months since signup")
ax.set_ylabel("Retention (fraction)")
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.3)
ax.legend(title="Cohort month")
st.pyplot(fig)

# Optional: include a table view of the matrix
with st.expander("Show retention matrix (raw)"):
    st.dataframe(cohort_matrix.style.format("{:.2f}"))

# Footer / notes
st.markdown("---")
st.markdown("**Notes:** This is a prototype; cohort matrix is produced by the EDA notebook. Extend filters to segment by plan, channel, or any user property.")
