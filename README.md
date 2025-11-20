# Fintech SaaS Churn Intelligence

**Author:** Chimmuanya Mogbo
**Project:** Cohort analysis, churn prediction & SHAP interpretability for a Fintech SaaS dataset

## Overview
This repository demonstrates a full churn analytics pipeline:
- Synthetic event generation and remapping to Telco-style customers
- Cohort analysis & retention matrices
- Feature engineering from event streams
- Baseline models (Logistic Regression, RandomForest, XGBoost)
- Explainability with SHAP and interactive Streamlit dashboard

## Repo structure
- `data/` — raw (ignored), processed, synthetic
- `notebooks/` — exploratory + modeling notebooks (Notebook 01, Notebook 02)
- `scripts/` — utilities (generate_synthetic_events.py, preprocess.py)
- `dashboard/` — Streamlit app
- `results/` — charts, model artifacts (not committed)

## How to run (quick)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# generate synthetic events
python scripts/generate_synthetic_events.py
# preprocess and build features
python scripts/preprocess.py
# run notebooks with jupyter lab
jupyter lab

```

## Notes
- Do not commit real customer data to this repository.

- Synthetic data files are included under data/synthetic/ for reproducibility.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


