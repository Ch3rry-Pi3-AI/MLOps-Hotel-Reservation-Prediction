# MLOps | Hotel Reservation Prediction (GCP)

End-to-end MLOps workflow for predicting hotel reservation cancellations, from ingestion to training and real-time inference.
Designed to reduce revenue loss, improve guest retention, and ship a reproducible ML pipeline with a containerized deployment path on GCP.

<p align="center">
  <img src="img/flask_app/hotel_reservation_app.gif" alt="Flask Inference App Demo" width="820">
</p>

## Why this project

- Reduce late cancellations with early risk signals.
- Improve revenue planning with consistent, measurable model performance.
- Ship an inference UI/API quickly with container-ready deployments.

## MLOps Flow

```mermaid
flowchart LR
    A[Hotel reservations CSV
GCS or local file] --> B[Data ingestion]
    B --> C[Raw artifacts]
    C --> D[Preprocessing
clean + encode + balance]
    D --> E[Processed features]
    E --> F[Training
LightGBM + MLflow]
    F --> G[Model artifact
lgbm_model.pkl]
    G --> H[Flask inference app]
```

## GCP Deployment Overview

```mermaid
flowchart LR
    User[Browser] --> CR[Cloud Run
Flask UI + API]
    CR --> GCS[(GCS: model + artifacts)]
    CR --> Logs[Cloud Logging]

    Train[Training pipeline
local or CI] --> GCS
    Train --> MLflow[MLflow Tracking]
    MLflow --> GCS

    Jenkins[Jenkins CI/CD
Docker-in-Docker] --> GCR[GCR]
    GCR --> CR
```

## Quick Start (Local)

1) Install prerequisites:
   - Python 3.10+
   - Docker (optional, for container runs)
   - gcloud CLI (optional, for GCP deployment)

2) Create a virtual environment and install dependencies:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3) Configure the pipeline:
   - Update `config/config.yaml` for your data source and feature settings.
   - Review `config/paths_config.py` for artifact locations.
   - If ingesting from GCS, set `GOOGLE_APPLICATION_CREDENTIALS` to your service account key JSON path.

4) Run end-to-end training:
```bash
python pipeline/training_pipeline.py
```

5) Launch the inference app:
```bash
python app.py
# open http://localhost:8080
```

## CI/CD Pipeline (Jenkins + GCP)

The main branch includes a Jenkins pipeline that automates build, test, containerization, and deployment to Cloud Run.

Stages (high level):
1) Setup Jenkins container (Docker-in-Docker)
2) GitHub integration
3) Dockerize the project
4) Create a venv inside Jenkins
5) Build image and push to GCR
6) Deploy to Cloud Run
7) Optional cleanup of cloud resources

See `custom_jenkins/README.md` for detailed setup steps, screenshots, and GCP credential configuration.

## Tech Stack

- Front end: HTML + CSS, Jinja2 templates.
- Back end: Flask (Python), model loading with joblib.
- ML: LightGBM, scikit-learn, SMOTE, MLflow tracking.
- MLOps: Docker, Jenkins CI/CD.
- GCP services: GCS, GCR, Cloud Run, IAM/Service Accounts, Cloud Logging.

## Project Structure

- `app.py`: Flask inference server and UI.
- `pipeline/`: End-to-end training pipeline entrypoint.
- `src/`: Ingestion, preprocessing, training modules.
- `config/`: YAML + params + paths configuration.
- `templates/` + `static/`: UI templates and CSS.
- `notebook/`: EDA and experimentation.
- `custom_jenkins/`: Jenkins DinD Dockerfile for CI/CD.
- `artifacts/`: Raw, processed, and model outputs.
- `mlruns/`: Local MLflow experiment tracking.
- `Dockerfile`, `Jenkinsfile`: container build + pipeline automation.

## Guides

- `config/README.md` - configuration details.
- `pipeline/README.md` - training pipeline flow.
- `src/README.md` - core modules and responsibilities.
- `templates/README.md` - UI template behavior.
- `static/README.md` - UI styling system.
- `custom_jenkins/README.md` - Jenkins DinD setup.
- `notebook/README.md` - notebook usage.
- `artifacts/README.md` - output layout.
- `utils/README.md` - shared helpers.

## Model Details (Concise)

- Target: `booking_status` (cancelled vs honored).
- Features: lead time, room type, special requests, pricing, and stay length.
- Preprocessing: label encoding, log transforms, SMOTE balancing.
- Training: LightGBM with RandomizedSearchCV.
- Metrics: accuracy, precision, recall, F1.

## License and Credits

- License: MIT (add `LICENSE` if needed).
- Dataset: Hotel Reservations Classification (Kaggle).
- Libraries: pandas, scikit-learn, imbalanced-learn, lightgbm, MLflow, Flask.
