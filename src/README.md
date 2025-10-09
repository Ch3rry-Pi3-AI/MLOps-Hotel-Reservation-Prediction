# 🧩 Source Code Directory — `src/`

This directory contains all **core Python modules** that define the functional backbone of the **MLOps Hotel Reservation Prediction** pipeline.
Each module performs a specific task, such as logging, data ingestion, preprocessing, or model training, while following consistent error handling and configuration patterns.

The `src/` folder ensures a clear separation between **code**, **configuration**, and **artifacts**, supporting modularity and ease of maintenance across all stages of the project.

## 📁 Folder Structure

```
mlops-hotel-reservation-prediction/
├── src/
│   ├── custom_exception.py      # Unified exception handling
│   ├── data_ingestion.py        # Downloads and splits raw data from GCP
│   ├── data_preprocessing.py    # Cleans, encodes, balances, and selects features
│   ├── logger.py                # Centralised logging configuration
│   └── model_training.py        # Trains LightGBM model and logs to MLflow
```

## 🎯 Overview of Modules

### 🧱 `logger.py`

Centralised logging configuration for the entire project.
It automatically creates daily log files under the `logs/` directory and timestamps each message for traceability.

**Key Features**

* Configures `INFO`-level logging globally.
* Stores logs in `logs/log_YYYY-MM-DD.log`.
* Provides a helper function `get_logger(name)` for consistent logging across modules.

**Example**

```python
from src.logger import get_logger
logger = get_logger(__name__)
logger.info("Data ingestion started.")
```



### ⚠️ `custom_exception.py`

Defines the `CustomException` class for descriptive, unified error handling.
Each raised exception automatically includes the **file name** and **line number** of the error, making debugging straightforward.

**Key Features**

* Wraps raw Python exceptions with contextual details.
* Integrates with the global logger for consistent reporting.
* Used throughout the pipeline for reliable tracebacks.

**Example**

```python
try:
    result = 10 / 0
except Exception as e:
    import sys
    raise CustomException(str(e), sys)
```



### ☁️ `data_ingestion.py`

Implements the `DataIngestion` class responsible for **downloading** the dataset from **Google Cloud Storage (GCS)**,
**splitting** it into training and testing subsets, and **saving** them under `artifacts/raw/`.

**Key Steps**

1. Connects to GCS via the `google-cloud-storage` client.
2. Downloads the raw CSV defined in `config/config.yaml`.
3. Splits the dataset into train/test based on a configured ratio.
4. Logs all operations and stores files locally.

**Example**

```python
from utils.common_functions import read_yaml
from config.paths_config import CONFIG_PATH
from src.data_ingestion import DataIngestion

cfg = read_yaml(CONFIG_PATH)
data_ingestion = DataIngestion(cfg)
data_ingestion.run()
```



### 🧹 `data_preprocessing.py`

Encapsulates the full **data preprocessing pipeline** inside the `DataProcessor` class.
It standardises cleaning, encoding, balancing, and feature selection before model training.

**Main Responsibilities**

* Drop irrelevant columns and duplicates.
* Apply Label Encoding for categorical variables.
* Handle skewed features using `log1p`.
* Balance classes via **SMOTE**.
* Select top-N features using **Random Forest** importance.
* Save processed data under `artifacts/processed/`.

**Example**

```python
from src.data_preprocessing import DataProcessor
from config.paths_config import *

processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
processor.process()
```

**Outputs**

* `processed_train.csv`
* `processed_test.csv`



### 🌳 `model_training.py`

Implements the `ModelTraining` class for **LightGBM model training**, **hyperparameter optimisation**, and **MLflow experiment tracking**.

**Pipeline Steps**

1. Loads preprocessed data from `artifacts/processed/`.
2. Runs `RandomizedSearchCV` for hyperparameter tuning.
3. Evaluates model performance (accuracy, precision, recall, F1).
4. Saves the best model to `artifacts/models/lgbm_model.pkl`.
5. Logs metrics, parameters, and artefacts to **MLflow**.

**Example**

```python
from src.model_training import ModelTraining
from config.paths_config import *

trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
trainer.run()
```

**MLflow Logs**

* Model parameters
* Evaluation metrics
* Dataset artefacts
* Trained model pickle



## 🧠 Design Principles

* **Separation of Concerns:** Each module handles a single, well-defined task.
* **Reusability:** All classes can be imported individually for debugging or testing.
* **Consistency:** Unified logging, error handling, and configuration access.
* **Traceability:** Each stage logs to file and uses `CustomException` for contextual errors.
* **Automation-Ready:** All modules are designed for pipeline execution within CI/CD systems (e.g., Jenkins or GitHub Actions).

## ✅ Summary

| Module                  | Responsibility                                   | Key Output                    |
| ----------------------- | ------------------------------------------------ | ----------------------------- |
| `logger.py`             | Centralised logging                              | Daily log files under `logs/` |
| `custom_exception.py`   | Unified error handling                           | Contextual exception messages |
| `data_ingestion.py`     | GCP data download and split                      | `train.csv`, `test.csv`       |
| `data_preprocessing.py` | Cleaning, encoding, balancing, feature selection | Processed CSVs                |
| `model_training.py`     | LightGBM training, evaluation, MLflow logging    | Trained model pickle          |