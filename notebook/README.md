# 📓 Exploratory Data Analysis & Experimentation — `notebook.ipynb`

This notebook documents the **exploratory data analysis (EDA)**, **data preprocessing**, and **machine learning experimentation** phases of the **Hotel Reservation Prediction** project.
It provides an interactive environment for early-stage insights, visual validation of preprocessing steps, and model prototyping before integration into the automated MLOps pipeline.

## 📁 File Location

```
mlops-hotel-reservation-prediction/
├── notebook/
│   └── notebook.ipynb
├── src/
├── pipeline/
├── config/
└── artifacts/
```

## 🎯 Purpose

The notebook serves as a **research and experimentation workspace** used to:

1. Explore the raw dataset and understand feature distributions.
2. Perform initial data cleaning and transformation steps.
3. Identify correlations and key predictors of booking cancellations.
4. Train and evaluate early machine learning models for benchmarking.
5. Refine insights that inform the automated pipeline’s configuration and feature engineering.

## 🧩 Structure Overview

| Section                        | Description                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- |
| **1. Data Loading**            | Imports and inspects the dataset, checking for nulls, dtypes, and duplicates.                             |
| **2. Exploratory Analysis**    | Visualises numerical and categorical variables, distributions, and correlations.                          |
| **3. Feature Engineering**     | Applies encoding, scaling, and transformation logic aligned with `data_processing` configuration.         |
| **4. Model Prototyping**       | Tests several classifiers (e.g. Logistic Regression, Random Forest, LightGBM) using small-scale training. |
| **5. Evaluation**              | Compares models with metrics such as accuracy, precision, recall, F1, and ROC-AUC.                        |
| **6. Observations & Insights** | Records findings that inform later pipeline stages.                                                       |

## ⚙️ Requirements

To open and run the notebook, activate the project’s virtual environment and install dependencies (if not already done):

```bash
uv venv
uv pip install -r requirements.txt
```

Then launch Jupyter:

```bash
jupyter notebook notebook/notebook.ipynb
```

## 🧠 Typical Workflow

1. Load configuration and dataset paths using `utils/common_functions.read_yaml()`.
2. Conduct visual exploration with libraries such as `pandas`, `matplotlib`, and `seaborn`.
3. Apply preliminary preprocessing consistent with `src/data_preprocessing.py`.
4. Run experiments to identify the best baseline model and parameters.
5. Record final insights and hyperparameter suggestions for use in the main training pipeline.

## 🧾 Outputs

| Output                 | Description                                                            |
| ---------------------- | ---------------------------------------------------------------------- |
| **EDA visualisations** | Histograms, boxplots, correlation heatmaps, and categorical summaries. |
| **Cleaned dataset**    | Intermediate DataFrame saved to `artifacts/processed/` for reuse.      |
| **Experiment results** | Performance metrics and confusion matrices for tested models.          |
| **Feature insights**   | Notes and visual confirmations for final feature selection.            |

## 🧩 Integration with MLOps Pipeline

The notebook acts as a **development sandbox** feeding into the automated scripts:

* Feature transformations tested here become part of `src/data_preprocessing.py`.
* Promising model configurations are migrated into `config/model_params.py`.
* Data paths mirror those defined in `config/paths_config.py` for consistency.

This ensures that interactive experimentation directly supports production-grade automation.

## ✅ Best Practices

* Keep cell outputs and plots clear and labelled for reproducibility.
* Save processed data and model outputs under `artifacts/` rather than within the notebook folder.
* Document all parameter changes and observations inside Markdown cells.
* Avoid hard-coded file paths — always import from `config/paths_config.py`.
* Use this notebook for exploration only; pipeline execution is handled by `pipeline/training_pipeline.py`.