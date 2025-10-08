# 🧩 **Training Pipeline — MLOps Hotel Reservation Prediction**

This branch connects all previous modules — **data ingestion**, **data preprocessing**, and **model training** — into a single, orchestrated workflow.
The new **pipeline script** automates the entire process from raw data to a trained model artefact, establishing a reproducible and maintainable structure for future automation and CI/CD integration.

This stage was made easier thanks to the **modular design** of the earlier stages and the prior **notebook experimentation**, which defined the logic now formalised into pipeline components.

## 🧾 **What’s New in This Stage**

* 🆕 **`pipeline/training_pipeline.py`** — a unified entrypoint that runs all stages sequentially:

  1. Data Ingestion
  2. Data Preprocessing
  3. Model Training
* 🧠 **Full automation** of the previously manual workflow — no need to run each module individually.
* 🔧 **`config/paths_config.py`** and existing modules are reused for consistent path and configuration management.
* 🪶 **Lighter README** since the logic remains unchanged — this stage focuses on orchestration.

## ⚙️ **How to Run the Full Pipeline**

After activating your virtual environment:

```bash
python pipeline/training_pipeline.py
```

This command will:

1. Ingest the raw data from your configured source
2. Preprocess and balance the dataset
3. Train and evaluate the LightGBM model
4. Save the trained model artefact to `artifacts/models/lgbm_model.pkl`
5. Log results and parameters to **MLflow**

## 🗂️ **Updated Project Structure**

```
mlops-hotel-reservation-prediction/
├── artifacts/
│   ├── raw/
│   ├── processed/
│   └── models/
│       └── lgbm_model.pkl
├── config/
│   ├── config.yaml
│   ├── paths_config.py
│   └── model_params.py
├── pipeline/
│   └── training_pipeline.py            # 🆕 Unified pipeline entrypoint
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   ├── logger.py
│   ├── custom_exception.py
│   └── __init__.py
├── utils/
│   └── common_functions.py
├── img/
│   └── model_training/
│       ├── mlflow_experiment.png
│       └── mlflow_run.png
├── notebooks/
│   └── notebook.ipynb
├── requirements.txt
├── setup.py
└── README.md
```

## 🚀 **Next Stage — Flask Application**

The next branch will focus on **creating a Flask application** to serve the trained model for real-time predictions.
This will involve:

* Loading the saved model (`artifacts/models/lgbm_model.pkl`)
* Building clean REST API endpoints
* Enabling integration with frontend interfaces or external systems

This stage marks the start of the **deployment layer** of your MLOps project — transitioning from model training to **model serving**.