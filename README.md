# 🏨 MLOps — Hotel Reservation Prediction

Predict booking outcomes end-to-end: ingest data → process → train → serve → ship.
This repository walks through the full MLOps lifecycle across sequential Git branches, so you can learn or reproduce the project one stage at a time.

<p align="center">
  <img src="img/flask_app/hotel_reservation_app.gif" alt="Flask Inference App Demo" width="820">
</p>

## Why this project?

Hotels lose revenue when bookings are cancelled late. A reliable predictor helps operations and revenue teams take action earlier.

### Core use-cases

* **Cancellation risk:** Predict whether a reservation will be cancelled so inventory can be double-protected (e.g., overbooking strategy) with lower risk.
* **Proactive retention:** Identify guests with medium–high risk and offer incentives (discount codes, upgrades) to reduce churn.
* **Fraud/abuse management:** Detect guests with a history of repeated cancellations and flag for manual review or potential bans.

## Project at a glance

* **Data:** Hotel reservation classification dataset (tabular).
* **Modelling:** LightGBM classifier with hyper-parameter search and MLflow tracking.
* **Serving:** Flask app for real-time inference.
* **CI/CD:** Jenkins (DinD) pipeline → build image → push to GCR → deploy to Cloud Run.

## Branch-by-branch roadmap

Each branch adds a focused layer. Check out branches in order to build the project progressively.

1. `00_project_setup` — Initial Project Setup
   Foundational Python package structure, centralised logging, custom exception handling, and repo hygiene.
2. `01_data_ingestion` — Data Ingestion from GCP
   Pull dataset from Google Cloud Storage, save raw extract, create train/test splits, and configure paths via YAML.
3. `02_notebook_experimentation` — Exploratory Analysis
   Jupyter notebook for EDA, preprocessing experiments, quick baselines, and feature importance exploration.
4. `03_data_processing` — Data Preprocessing
   Production-ready script that cleans, encodes, balances (SMOTE), and selects features. Outputs processed train/test CSVs.
5. `04_model_training` — Model Training
   Train a LightGBM model with RandomizedSearchCV, evaluate on hold-out data, persist artefacts, and log to MLflow.
6. `05_training_pipeline` — Unified Training Pipeline
   Orchestrate ingestion → processing → training via a single pipeline entrypoint to ensure repeatability.
7. `06_flask_app` — Inference Serving
   Flask application that loads the trained model and serves a web form + prediction endpoint.
8. `07_cicd_pipeline` — CI/CD Automation
   Jenkins-in-Docker pipeline to build, push, and deploy the container to Google Cloud Run.

## How to follow along locally

```bash
# 1) Clone once
git clone <your-repo-url>
cd mlops-hotel-reservation-prediction

# 2) Start from the beginning
git checkout 00_project_setup

# 3) Progress step-by-step
git checkout 01_data_ingestion
git checkout 02_notebook_experimentation
git checkout 03_data_processing
git checkout 04_model_training
git checkout 05_training_pipeline
git checkout 06_flask_app
git checkout 07_cicd_pipeline
```

## Quickstart (main branch)

### 1) Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2) Configuration

Set the paths and parameters in `config/config.yaml` and `config/paths_config.py`.
For GCP access (data ingestion), set `GOOGLE_APPLICATION_CREDENTIALS` to your service-account key path.

### 3) Run end-to-end training (pipeline)

```bash
python pipeline/training_pipeline.py
```

This will:

* Ingest data (from configured source)
* Process data (clean, encode, balance, select features)
* Train and evaluate LightGBM
* Save model to `artifacts/models/lgbm_model.pkl`
* Log run to MLflow

### 4) Launch the Flask app (inference)

```bash
python app.py
# open http://localhost:8080
```

Enter booking details to get an instant prediction (cancel / honour).
The GIF at the top shows the expected flow.

## 📁 Actual Project Structure

```
mlops-hotel-reservation-prediction/
├── artifacts/
├── config/
│   ├── config.yaml
│   ├── model_params.py
│   └── paths_config.py
├── custom_jenkins/
│   └── Dockerfile
├── img/
├── logs/
├── MLOps_Hotel_Reservation_Prediction.egg-info/
├── mlruns/
├── notebook/
│   ├── notebook.ipynb
│   └── random_forest.pkl
├── pipeline/
│   └── training_pipeline.py
├── src/
│   ├── custom_exception.py
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   ├── logger.py
│   └── model_training.py
├── static/
│   └── style.css
├── templates/
│   └── index.html
├── utils/
│   └── common_functions.py
├── venv/
├── .gitignore
├── app.py
├── Dockerfile
├── Jenkinsfile
├── requirements.txt
└── setup.py
```

## ML details (concise)

* **Target:** `booking_status` (cancelled vs honoured).
* **Features:** Mix of numeric and categorical booking attributes (lead time, room type, special requests, etc.).
* **Preprocessing:** Label encoding, skewness handling, SMOTE for class balance, feature selection via Random Forest importance.
* **Model:** LightGBM with search over learning rate, leaves, depth, etc.
* **Metrics:** Accuracy, Precision, Recall, F1 on held-out test set.
* **Tracking:** MLflow for parameters, metrics, artefacts.

## CI/CD overview (Jenkins → Cloud Run)

* Jenkins (DinD) builds and tests the project.
* Builds a Docker image and pushes to Google Container/Artifact Registry.
* Deploys to Google Cloud Run (fully managed, autoscaling).
* Outputs a public service URL for the Flask API/UI.

## Open-source licence

This project is released under the **MIT License**.
You are free to use, modify, and distribute the code with attribution.
A `LICENSE` file can be added to the repository root with the full MIT text if needed.

## Acknowledgements

* Dataset: Hotel Reservations Classification (Kaggle)
* Libraries: pandas, scikit-learn, imbalanced-learn, lightgbm, MLflow, Flask