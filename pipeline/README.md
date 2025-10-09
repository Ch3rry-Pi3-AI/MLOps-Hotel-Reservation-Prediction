# 🧠 Training Pipeline — `training_pipeline.py`

This script serves as the **main entrypoint** for executing the complete **Hotel Reservation Prediction** workflow.
It orchestrates all major stages of the MLOps pipeline — from raw data ingestion to final model training — in a single, reproducible process.

## 📁 File Location

```
mlops-hotel-reservation-prediction/
├── pipeline/
│   └── training_pipeline.py
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py
│   └── model_training.py
├── config/
│   ├── config.yaml
│   ├── model_params.py
│   └── paths_config.py
└── utils/
    └── common_functions.py
```

## 🎯 Purpose

The `training_pipeline.py` script brings together all modular components of the project into a single executable pipeline.
It ensures that each stage is run sequentially and configured consistently, using the settings defined in the YAML configuration files under the `config/` directory.

**Pipeline Stages**

1. **Data Ingestion** – Reads the raw dataset from cloud storage (GCP bucket) or local artifacts and splits it into training and test sets.
2. **Data Preprocessing** – Cleans, transforms, and encodes the data according to configuration parameters.
3. **Model Training** – Trains a LightGBM model using optimised hyperparameters and saves the model artifact.

## ⚙️ Usage

From the project root, run:

```bash
python pipeline/training_pipeline.py
```

This will automatically:

* Load configuration settings from `config/config.yaml`
* Generate training and test datasets under `artifacts/raw/`
* Produce processed data under `artifacts/processed/`
* Train a LightGBM model and save it to `artifacts/models/lgbm_model.pkl`

## 🧩 Integrated Modules

| Stage                      | Module                                 | Description                                      |
| -------------------------- | -------------------------------------- | ------------------------------------------------ |
| **1️⃣ Data Ingestion**     | `src.data_ingestion.DataIngestion`     | Downloads and splits the dataset.                |
| **2️⃣ Data Preprocessing** | `src.data_preprocessing.DataProcessor` | Handles feature cleaning, encoding, and scaling. |
| **3️⃣ Model Training**     | `src.model_training.ModelTraining`     | Trains and serialises the model using LightGBM.  |

Each of these modules is designed to be reusable and can be executed independently or through this unified script.

## 🧾 Configuration Files

| File                     | Purpose                                                                           |
| ------------------------ | --------------------------------------------------------------------------------- |
| `config/config.yaml`     | Defines ingestion ratios, categorical/numerical columns, and preprocessing rules. |
| `config/model_params.py` | Contains LightGBM and RandomizedSearchCV parameters for model tuning.             |
| `config/paths_config.py` | Centralises all file paths for raw, processed, and model artifacts.               |

The pipeline automatically imports these configurations through `utils/common_functions.read_yaml()`.

## 🧠 Design Principles

* **Modular Execution:** Each step is its own class for better maintainability.
* **Config-Driven:** Parameters are externalised in YAML, keeping the pipeline flexible.
* **Reproducible Outputs:** Every run produces deterministic outputs under `artifacts/`.
* **Seamless Logging:** All stages log progress through the central logger (`src/logger.py`).
* **Error Resilience:** Failures are caught and wrapped in the custom exception handler (`src/custom_exception.py`).

## ✅ Example Run Output

Example console output when executing the pipeline:

```
INFO - Starting data ingestion...
INFO - Data successfully split into train (80%) and test (20%)
INFO - Beginning preprocessing of training data...
INFO - Data transformed and saved to artifacts/processed/
INFO - Training LightGBM model with 5 random hyperparameter sets
INFO - Best model saved to artifacts/models/lgbm_model.pkl
INFO - Pipeline completed successfully.
```

## 🚀 Outcome

After running this pipeline, the project generates:

| Artifact            | Path                              | Description                              |
| ------------------- | --------------------------------- | ---------------------------------------- |
| **Train/Test Data** | `artifacts/raw/`                  | Split datasets ready for processing      |
| **Processed Data**  | `artifacts/processed/`            | Cleaned and encoded features             |
| **Trained Model**   | `artifacts/models/lgbm_model.pkl` | Final LightGBM model ready for inference |

## 🧩 Example Code Reference

```python
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()
```

## 💡 Best Practices

* Always confirm the GCP bucket and file name in `config.yaml` before running.
* Clean the `artifacts/` directory between major runs if testing new configurations.
* Use version control on the YAML and model parameter files to track experimental changes.
* Integrate this pipeline into CI/CD (Jenkins or GitHub Actions) for automated retraining.