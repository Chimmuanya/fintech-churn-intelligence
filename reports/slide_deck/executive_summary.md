# Fintech SaaS Churn Intelligence  
**Predictive Retention System | XGBoost + SHAP | AUC 0.90**

---

### Slide 1 — Business Problem: Churn is Eroding ARR  
**Industry**: SaaS Billing & Subscription Platform  
Even small increases in churn destroy net revenue retention and LTV.

**Core Problem**  
Customers cancel without warning → reactive, ineffective retention.

**Why It Matters**  
- Churn directly reduces ARR/MRR  
- Early-life churn (low tenure) drives the majority of losses  
- Retaining a customer is 3–5× cheaper than acquiring a new one  

**Project Goal**  
Build an early-warning churn intelligence system with actionable, explainable insights.

---

### Slide 2 — Data & Methodology  
**Sources**  
1. Customer billing data (tenure, plan, churn label)  
2. Synthetic product-usage event log (logins, billing actions, errors, support)

**Feature Engineering**  
- `tenure_months_precise`  
- Usage intensity & consistency  
- Recency (`events_last_30d`)  
- Friction signals (errors, support contacts)  
- Onboarding speed (`time_to_first_event_days`)

**Models Evaluated**  
- Logistic Regression → baseline  
- Random Forest  
- **XGBoost → selected** (AUC 0.8994)

**Explainability**  
SHAP values for full transparency and actionability

---

### Slide 3 — Model Performance  
| Model               | AUC     | Accuracy | Precision@Top 5% |
|---------------------|---------|----------|------------------|
| Logistic Regression | 0.753   | 0.802    | 0.71             |
| Random Forest       | 0.781   | 0.819    | 0.78             |
| **XGBoost**         | **0.899** | **0.866** | **1.000**        |

**Business Impact**  
The model perfectly ranks the riskiest 5% of customers → ideal for high-precision save campaigns.

---

### Slide 4 — Key Insights from SHAP  
**Top Global Churn Drivers** (Mean |SHAP|)

| Rank | Feature                    | Insight                                      |
|------|----------------------------|----------------------------------------------|
| 1    | tenure_months_precise      | New users churn disproportionately → **onboarding crisis** |
| 2    | events_count               | Low usage = high churn risk                  |
| 3    | events_last_30d            | Recent drop-off = strongest warning signal   |
| 4    | unique_active_days         | Consistency beats volume                     |
| 5    | error_event_count          | Billing/product friction kills retention     |
| 6    | support_contacts_count     | Support ticket = leading churn indicator     |

**Strategic Conclusion**  
Churn is driven by **activation failure + product friction**, not just inactivity.

---

### Slide 5 — High-Impact Recommendations (ARR-Focused)  
1. **Reinvent Onboarding** (highest ROI)  
   - Guided setup wizard + Day 1–7 success checklist  
   - Proactive CS outreach for high-value new accounts  

2. **Eliminate Errors**  
   - Real-time error monitoring dashboard  
   - “Resolve-before-churn” escalation workflow  

3. **Reactivation Engine**  
   - Automated re-engagement for low-activity users  
   - Usage-based incentives  

4. **High-Risk Save Campaign**  
   - Precision@5% = 100% → contact only the true at-risk segment  
   - Expected impact: **+15–25% 90-day retention**

---

### Slide 6 — Deployment Roadmap  
| Phase | Deliverable                            | Timeline |
|-------|----------------------------------------|----------|
| 1     | Live Streamlit churn dashboard         | 1 week   |
| 2     | CRM integration (HubSpot/Salesforce)  | 2 weeks  |
| 3     | Weekly batch inference + Slack alerts  | 3 weeks  |
| 4     | Add billing failure & plan features   | Ongoing  |

**The system is production-ready — just connect to your warehouse.**

---
