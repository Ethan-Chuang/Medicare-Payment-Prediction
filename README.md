# Medicare Utilization Analysis

An inferential machine-learning project that turns public **Medicare Current
Beneficiary Survey (MCBS)** data into insight about *what drives how much
beneficiaries use Medicare*. It builds a single "utilization score" for each
beneficiary, predicts it with a range of regression models, and — more
importantly — explains **which factors** move that score and by how much.

> Author: **Ethan Chuang**. Built as a course project in inferential modeling.

---

## What it does

1. **Merges** four years (2020–2023) of MCBS Survey File data (fall + winter).
2. **Cleans** ~577 raw columns down to ~58 modeling variables, split into
   *utilization* variables (how much care someone used) and *predictor*
   variables (demographics, administrative status, access to care).
3. **Builds a target** — a continuous *utilization score* — by running the
   utilization variables through **PCA** and taking the first component (PC1),
   then normalizing and log-transforming it.
4. **Trains and compares** nine regression models with cross-validation.
5. **Explains** the results with feature importances and **SHAP** values, and
   ships a `predict_with_explanation()` function that scores a single
   beneficiary and lists the top factors behind the prediction.

---

## Data

- **Source:** [Medicare Current Beneficiary Survey (MCBS)](https://www.cms.gov/data-research/research/medicare-current-beneficiary-survey),
  Survey File Public Use File, U.S. Centers for Medicare & Medicaid Services (CMS).
- **Coverage:** 2020–2023, fall and winter files merged on `PUF_ID`
  (~43,000 rows × 577 columns → ~38,000 rows × 58 columns after cleaning).
- **Codebooks:** the two files in `codebooks/` document every variable.

> ⚠️ The raw survey `.csv` files are **not** included in this repo — only the
> codebooks. Download the Survey File PUFs for each year from CMS to reproduce
> the analysis (see [Running it](#running-it)).

*Citation:* Centers for Medicare & Medicaid Services. *Medicare Current
Beneficiary Survey (MCBS).* U.S. Department of Health & Human Services.

---

## Method

| Stage | What happens |
|---|---|
| **Cleaning** | Drop survey-weight columns (`PUFF*`/`PUFW*`), select high-signal variables, handle missingness |
| **EDA** | Missingness chart, correlation heatmap, and **VIF** to flag multicollinearity |
| **Target** | PCA on utilization variables → PC1 → sign-fixed, normalized, log-transformed *utilization score* |
| **Split** | Stratified train/test split (target binned into quartiles with `qcut`) |
| **Preprocessing** | Median imputation + standard scaling, fit on train only |
| **Baseline** | `statsmodels` OLS with a significance table (27 of 36 predictors significant) |
| **Models** | Cross-validated comparison of nine regressors |
| **Explainability** | XGBoost feature importances, SHAP values, and an OLS vs XGBoost vs SHAP ranking comparison |

### Models compared

Linear Regression, Ridge, Lasso, ElasticNet, Decision Tree, Random Forest,
Gradient Boosting, and XGBoost.

**Results (test R², best first):**

| Model | Test R² | CV R² | Overfit gap | RMSE | MAE |
|---|---|---|---|---|---|
| **Gradient Boosting** | **0.525** | 0.516 | 0.014 | 0.651 | 0.485 |
| XGBoost | 0.523 | 0.514 | 0.002 | 0.652 | 0.485 |
| Random Forest | 0.515 | 0.506 | 0.035 | 0.658 | 0.489 |
| Linear Regression / Ridge | 0.503 | 0.495 | −0.006 | 0.666 | 0.484 |
| Decision Tree | 0.493 | 0.485 | 0.007 | 0.673 | 0.499 |
| ElasticNet | 0.471 | 0.467 | −0.004 | 0.687 | 0.502 |
| Lasso | 0.435 | 0.431 | −0.004 | 0.710 | 0.522 |

The two gradient-boosting models perform best; XGBoost is notable for a near-zero
overfit gap, indicating it generalizes well.

---

## Key findings

Across OLS coefficients, XGBoost importances, and SHAP values, three predictors
consistently rise to the top:

- **`ADM_FFS_FLAG_YR`** — whether the beneficiary was in **Fee-for-Service**
  (traditional Parts A & B) vs **Medicare Advantage** (Part C). This is by far
  the strongest predictor of utilization.
- **`ACW_CARESPCL`** — whether the beneficiary sees a **specialist** outside
  their primary care provider.
- **`DEM_AGE`** — the beneficiary's **age**.

The dominance of the FFS-vs-MA flag suggests the *type* of Medicare coverage is
tightly linked to how much care a beneficiary uses.

---

## Predicting a single beneficiary

`predict_with_explanation(patient_data)` takes one beneficiary's feature values
and returns the predicted utilization score, a `LOW`/`MODERATE`/`HIGH` risk
level, and the top SHAP-ranked factors with their direction of impact — turning
the model into an explainable, per-person tool.

---

## Repository structure

```
Medicare-Payment-Prediction/
├── README.md
├── requirements.txt
├── LICENSE
├── medicare_utilization_analysis.ipynb   # main analysis notebook (start here)
├── medicare_utilization_analysis.html    # rendered notebook (view without running)
├── Medicare Payment Prediction.py        # standalone data-loading / cleaning script
└── codebooks/
    ├── MCBSPUF_2023_1_fall_codebook.txt   # variable codebook — fall file
    └── MCBSPUF_2023_2_winter_codebook.txt # variable codebook — winter file
```

The quickest way to read the project without running anything is to open
`medicare_utilization_analysis.html` in a browser.

---

## Running it

**Requirements** (Python 3.9+):

```bash
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels xgboost shap
```

**Steps:**

1. Download the **MCBS Survey File** Public Use Files for 2020–2023 (fall and
   winter) from [CMS](https://www.cms.gov/data-research/research/medicare-current-beneficiary-survey).
2. Update the file paths near the top of the notebook — they currently point at
   a local machine (e.g. `/Users/ethanc/medicare project/...`) — to wherever you
   saved the data.
3. Open and run `medicare_utilization_analysis.ipynb` top to bottom.

---

## Limitations & next steps

- This is an **inferential** study: it surfaces associations and relative
  feature importance, **not causal claims**. Survey data carries selection and
  self-report bias.
- Data paths are currently hard-coded; a small config or CLI would make the
  notebook portable.
- **Next step** (from the project's conclusion): build an interactive dashboard
  to visualize results and test predictions on new inputs.

---

*Educational project using public CMS data. Not affiliated with or endorsed by
CMS.*
