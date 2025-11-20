# dashboard/app.py
"""
Streamlit dashboard for Fintech Churn Intelligence
- Designed for Streamlit Cloud (commit artifacts to repo)
- Loads precomputed artifacts: cohort_matrix.csv, shap_importance_xgboost.csv, predictions_xgboost.csv
- Loads a saved model artifact for optional on-the-fly scoring if small
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO

# Page config
st.set_page_config(page_title="Churn Intelligence — Cohorts & Risk", layout="wide")

# -------------------------
# Cached I/O helpers
# -------------------------
@st.cache_data(ttl=3600)  # cache for 1 hour
def load_csv(path):
    return pd.read_csv(path, index_col=0)

@st.cache_resource
def load_model(path):
    # load lightweight model artifact (joblib)
    model = joblib.load(path)
    return model

# -------------------------
# Paths (commit these small artifacts into repo)
# -------------------------
COHORT_CSV = "results/charts/cohort_matrix.csv"
SHAP_CSV = "results/models/shap/shap_importance_random_forest.csv"
PRED_CSV = "results/models/predictions_random_forest.csv"
MODEL_FILE = "results/models/xgboost.joblib"  # optional

# -------------------------
# Top-level UI
# -------------------------
st.title("Fintech Churn Intelligence — Cohorts & Risk")
st.write("Interactive dashboard for cohort retention, risk scoring and top churn drivers. Designed for SaaS billing platforms.")

# Sidebar filters
st.sidebar.header("Controls")
show_model = st.sidebar.checkbox("Enable on-the-fly scoring (loads model)", value=False)
top_k = st.sidebar.slider("Top risk users to show", min_value=10, max_value=500, value=50, step=10)
cohorts_to_show = st.sidebar.slider("Cohorts to show", min_value=3, max_value=12, value=6)

# -------------------------
# Load cohort matrix
# -------------------------
try:
    cohort_matrix = load_csv(COHORT_CSV)
    # attempt to parse index to datetime if stringified
    try:
        cohort_matrix.index = pd.to_datetime(cohort_matrix.index)
    except Exception:
        pass
except Exception as e:
    st.error(f"Could not load cohort matrix: {e}")
    st.stop()

# Retention visualization
st.header("Cohort Retention")
st.markdown("Retention matrix (rows = signup month, columns = months since signup).")
with st.expander("Show retention matrix raw"):
    st.dataframe(cohort_matrix.style.format("{:.2f}"))

# plot retention curves with Plotly for interactivity
recent_cohorts = cohort_matrix.index[-cohorts_to_show:]
fig = px.line(
    x=list(range(cohort_matrix.shape[1])),
    y=[cohort_matrix.loc[c].values for c in recent_cohorts],
    labels={'x':'Months since signup', 'y':'Retention'},
    title=f"Retention Curves — last {cohorts_to_show} cohorts"
)
# plotly expects tidy traces; add manually
fig = px.line()
for c in recent_cohorts:
    fig.add_scatter(x=list(range(cohort_matrix.shape[1])), y=cohort_matrix.loc[c].values, mode='lines+markers', name=str(pd.to_datetime(c).date()))
fig.update_layout(yaxis_tickformat=".0%", yaxis_range=[0,1.05])
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Risk-ranked users table
# -------------------------
st.header("Top Risk Users")
st.markdown("This table shows the highest-risk customers from the test/holdout set (precomputed).")

try:
    preds = pd.read_csv(PRED_CSV)
    # ensure columns: user_id, y_true, prob_churn
    preds = preds.sort_values("prob_churn", ascending=False).reset_index(drop=True)
except Exception as e:
    st.warning("Predictions file not found or unreadable. Optionally enable model scoring.")
    preds = pd.DataFrame(columns=["user_id","y_true","prob_churn"])

# allow dynamic scoring if model available and requested
if show_model:
    try:
        model = load_model(MODEL_FILE)
        st.success("Model loaded (on-the-fly scoring enabled).")
        st.caption("On-the-fly scoring uses the model in repo; heavy models may slow the app.")
    except Exception as e:
        st.error(f"Failed to load model for on-the-fly scoring: {e}")

# show the top_k risky users
if not preds.empty:
    st.dataframe(preds.head(top_k).style.format({"prob_churn":"{:.3f}"}))
    csv = preds.head(top_k).to_csv(index=False).encode('utf-8')
    st.download_button("Download top risk CSV", data=csv, file_name="top_risk_users.csv", mime="text/csv")
else:
    st.info("No precomputed predictions available. Enable model scoring or upload predictions CSV.")

# -------------------------
# SHAP importance (precomputed)
# -------------------------
st.header("Global Feature Importance (SHAP)")
st.markdown("Precomputed mean(|SHAP|) values — use this when SHAP is expensive to compute live.")

try:
    shap_imp = pd.read_csv(SHAP_CSV)
    # show top 10
    st.bar_chart(shap_imp.sort_values("mean_abs_shap", ascending=True).set_index("feature")["mean_abs_shap"].tail(10))
    st.dataframe(shap_imp.sort_values("mean_abs_shap", ascending=False).head(12).style.format({"mean_abs_shap":"{:.4f}"}))
except Exception as e:
    st.warning(f"SHAP importance file missing: {e}")

# Footer / notes
st.markdown("---")
st.caption("This is a prototype dashboard. For production, connect to a DB and implement auth + logging.")
