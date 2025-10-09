# ⚙️ Configuration Directory — `config/`

This folder defines all global configuration files for the **MLOps Hotel Reservation Prediction** project.
It centralises paths, hyperparameters, and dataset settings used across every stage of the pipeline — ensuring consistency, reproducibility, and easy maintenance.

The configuration files are lightweight, version-controlled, and automatically loaded at runtime through the utility module `utils/common_functions.py`.

## 📁 Folder Structure

```
mlops-hotel-reservation-prediction/
├── config/
│   ├── config.yaml          # Core project configuration (data ingestion & preprocessing)
│   ├── model_params.py      # Model hyperparameter definitions (LightGBM + RandomSearchCV)
│   └── paths_config.py      # Centralised file path configuration for all pipeline stages
```

## 🧩 config.yaml — Project Parameters

This YAML file defines static configuration values used by different pipeline components.
It separates high-level parameters from code, making it easier to adapt the project to new environments or datasets.

**Key Sections**

| Section             | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **data_ingestion**  | GCP bucket name, dataset filename, and train/test split ratio.                              |
| **data_processing** | Lists of categorical and numerical columns, skewness threshold, and number of top features. |

**Example Content**

```yaml
data_ingestion:
  bucket_name: "mlops-hotel-reservation-prediction-bucket"
  bucket_file_name: "Hotel_Reservations.csv"
  train_ratio: 0.8

data_processing:
  categorical_columns:
    - type_of_meal_plan
    - required_car_parking_space
    - room_type_reserved
    - market_segment_type
    - repeated_guest
    - booking_status

  numerical_columns:
    - no_of_adults
    - no_of_children
    - no_of_weekend_nights
    - no_of_week_nights
    - lead_time
    - arrival_year
    - arrival_month
    - arrival_date
    - no_of_previous_cancellations
    - no_of_previous_bookings_not_canceled
    - avg_price_per_room
    - no_of_special_requests

  skewness_threshold: 5
  no_of_features: 10
```

**Loaded in code via**

```python
from utils.common_functions import read_yaml
cfg = read_yaml("config/config.yaml")
```

## 🌳 model_params.py — Model Hyperparameters

Defines the LightGBM parameter search space and RandomizedSearchCV configuration used during model training.
This design allows easy experimentation without editing training scripts.

**Main Dictionaries**

| Name                   | Description                                                               |
| ---------------------- | ------------------------------------------------------------------------- |
| `LIGHTGBM_PARAMS`      | Parameter ranges (e.g. `max_depth`, `learning_rate`, `num_leaves`).       |
| `RANDOM_SEARCH_PARAMS` | Search control settings (e.g. `n_iter`, `cv`, `scoring`, `random_state`). |

**Example**

```python
from config.model_params import LIGHTGBM_PARAMS, RANDOM_SEARCH_PARAMS
```

**LightGBM Parameters (Search Space)**

```python
LIGHTGBM_PARAMS = {
    'n_estimators': randint(100, 500),
    'max_depth': randint(5, 50),
    'learning_rate': uniform(0.01, 0.2),
    'num_leaves': randint(20, 100),
    'boosting_type': ['gbdt', 'dart']
}
```

**Random Search Configuration**

```python
RANDOM_SEARCH_PARAMS = {
    'n_iter': 5,
    'cv': 2,
    'n_jobs': -1,
    'verbose': 2,
    'random_state': 5901,
    'scoring': 'accuracy'
}
```

## 🧾 paths_config.py — Path Management

Centralises all data, model, and configuration paths used throughout the project.
It ensures each pipeline stage writes to a predictable, organised directory structure.

**Example Imports**

```python
from config.paths_config import (
    RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH,
    PROCESSED_TRAIN_DATA_PATH, MODEL_OUTPUT_PATH, CONFIG_PATH
)
```

**Defined Paths**

| Category            | Variable                                                | Description                         |
| ------------------- | ------------------------------------------------------- | ----------------------------------- |
| **Data Ingestion**  | `RAW_FILE_PATH`, `TRAIN_FILE_PATH`, `TEST_FILE_PATH`    | Raw and split datasets.             |
| **Data Processing** | `PROCESSED_TRAIN_DATA_PATH`, `PROCESSED_TEST_DATA_PATH` | Cleaned training and test data.     |
| **Model Training**  | `MODEL_OUTPUT_PATH`                                     | Serialized LightGBM model artifact. |
| **Configuration**   | `CONFIG_PATH`                                           | Path to `config.yaml`.              |

**Directory Structure (auto-created)**

```
artifacts/
├── raw/
│   ├── raw.csv
│   ├── train.csv
│   └── test.csv
├── processed/
│   ├── processed_train.csv
│   └── processed_test.csv
└── models/
    └── lgbm_model.pkl
```

**Automatic Directory Creation**

```python
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
```

## 🧠 Design Philosophy

* **Single Source of Truth:** All pipeline parameters, file paths, and hyperparameters are defined here.
* **Reproducibility:** Enables version-controlled experiments without modifying source code.
* **Portability:** Easy migration to other cloud environments (e.g. AWS, Azure) by editing only `config.yaml`.
* **Consistency:** Standardised path handling prevents hard-coded file references in scripts.

## ✅ Summary

| File                | Purpose                                                       |
| ------------------- | ------------------------------------------------------------- |
| **config.yaml**     | Controls ingestion and preprocessing logic.                   |
| **model_params.py** | Defines model hyperparameter ranges and search configuration. |
| **paths_config.py** | Centralises all file paths for data and model artefacts.      |