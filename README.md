# 🧠 **Exploratory Analysis — MLOps Hotel Reservation Prediction**

This branch represents the **data scientist’s experimental stage**, where the **Hotel Reservations dataset** (previously ingested from Google Cloud Storage) is explored, cleaned, and analysed within a **Jupyter Notebook** environment.

The purpose of this stage is to **understand the data**, perform **EDA and preprocessing experiments**, and identify **key modelling strategies** — before the workflow is modularised and automated by an ML engineer in the next stage.



## 🧾 **What This Stage Includes**

* ✅ Jupyter Notebook (`notebooks/notebook.ipynb`) for interactive exploration
* ✅ Initial data validation (missing values, duplicates, column inspection)
* ✅ Exploratory data analysis (univariate, bivariate, and correlation)
* ✅ Preprocessing (encoding, transformations, feature checks)
* ✅ Class balancing using **SMOTE**
* ✅ Baseline modelling with multiple ML algorithms
* ✅ Random Forest feature importance and quick hyperparameter tuning
* ✅ Final model persistence (`random_forest.pkl`) for downstream use

This notebook acts as a **sandbox** for a data scientist — a place to experiment freely before refactoring the workflow into modular scripts and pipeline stages.



## 🗂️ **Updated Project Structure**

```
mlops-hotel-reservation-prediction/
├── artifacts/
│   ├── raw/                        # From previous data ingestion stage
│       ├── raw.csv
│       ├── train.csv
│       └── test.csv
├── notebooks/
│   └── notebook.ipynb              # 🔍 Data scientist EDA & experimentation
├── config/
│   ├── config.yaml
│   └── paths_config.py
├── src/
│   ├── data_ingestion.py
│   ├── logger.py
│   ├── custom_exception.py
│   └── __init__.py
├── utils/
│   └── common_functions.py
├── requirements.txt
├── setup.py
└── README.md                       # 📖 You are here
```

> 💡 The notebook uses `artifacts/raw/train.csv` and `test.csv` generated in the previous **Data Ingestion from GCP** stage.



## 🧩 **Notebook Highlights**

Within `notebooks/notebook.ipynb`, you’ll find clearly documented sections covering:

1. **Setup & Imports** — all required libraries configured for reproducibility
2. **Data Loading** — reads from `artifacts/raw/train.csv`
3. **Exploratory Data Analysis (EDA)** — distributions, correlations, relationships
4. **Preprocessing & Encoding** — label encoding, skewness correction, VIF check
5. **Class Balancing** — SMOTE applied to address booking imbalance
6. **Modelling Experiments** — Random Forest, Gradient Boosting, Logistic Regression, etc.
7. **Hyperparameter Tuning** — lightweight `RandomizedSearchCV` example
8. **Model Persistence** — saves `random_forest.pkl` for inference or modular pipelines



## 🚀 **Next Stage — Modular Data Processing**

In the next branch, the **data scientist’s experimental workflow** will be translated into a **modular, production-ready data processing pipeline**:

* Code moved from notebook → `src/data_processing/` modules
* Configurable parameters defined in YAML
* Unit tests and CI integration added
* Integration with MLflow and model registry prepared

This marks the transition from **exploration → engineering** — bridging experimentation and full MLOps automation.
