# 🧰 **Utility Module — `common_functions.py`**

This module provides **shared helper functions** for configuration handling and dataset loading across the **MLOps Hotel Reservation Prediction** project.

It standardises how configuration files and data sources are accessed, ensuring **reproducible** and **traceable** operations through consistent logging and structured exception management.



## 🗂️ **File Location**

```
mlops-hotel-reservation-prediction/
├── src/
│   ├── logger.py
│   ├── custom_exception.py
├── config/
│   ├── paths_config.py
│   └── config.yaml
├── utils/
│   └── common_functions.py   # 🧰 Shared YAML & CSV utilities
└── artifacts/
    └── raw/
        └── train.csv
```



## 🎯 **Purpose**

The `common_functions.py` module centralises **two key utilities** used throughout the pipeline:

| Function      | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| `read_yaml()` | Loads and parses project configuration files (`config.yaml`). |
| `load_data()` | Loads raw CSV datasets into Pandas DataFrames for processing. |

These utilities are integrated into other modules like `data_ingestion.py` and `data_preprocessing.py` to maintain a unified and reliable data access pattern.



## ⚙️ **Dependencies**

| Type                 | Modules Used                                                |
| -------------------- | ----------------------------------------------------------- |
| **Standard Library** | `os`, `sys`                                                 |
| **Third-Party**      | `yaml`, `pandas`                                            |
| **Internal**         | `src.logger`, `src.custom_exception`, `config.paths_config` |



## 🔧 **Function Overview**

### 1️⃣ `read_yaml(file_path: str = CONFIG_PATH) -> dict`

Reads and validates a YAML configuration file (defaults to `config/config.yaml`).
Returns a dictionary containing configuration parameters such as data paths, model settings, and pipeline options.

**Example:**

```python
from utils.common_functions import read_yaml

cfg = read_yaml()
print(cfg["data"]["train_path"])
```

**Key Features:**

* Logs success or error using the central project logger.
* Raises `CustomException` if the file is missing or unreadable.
* Uses `yaml.safe_load` for secure parsing.

**Output Example:**

```text
INFO - Successfully read YAML config: config/config.yaml
```



### 2️⃣ `load_data(csv_path: str) -> pd.DataFrame`

Loads a CSV dataset into a Pandas DataFrame and validates that it was read successfully.

**Example:**

```python
from utils.common_functions import load_data

train_df = load_data("artifacts/raw/train.csv")
print(train_df.shape)
```

**Key Features:**

* Logs dataset load path and resulting shape.
* Returns a clean, ready-to-process DataFrame.
* Raises `CustomException` for missing or corrupt files.

**Output Example:**

```text
INFO - Loading data from: artifacts/raw/train.csv
INFO - Data loaded successfully: shape=(4040, 22)
```



## 🧱 **Error Handling & Logging**

Both functions rely on:

* `src/logger.get_logger()` → ensures structured log output for all modules.
* `src/custom_exception.CustomException` → wraps system errors with descriptive messages.

**Example Log:**

```text
ERROR - Error while loading data from 'artifacts/raw/missing.csv': File not found
```

This allows errors to be captured in your daily logs (`logs/log_YYYY-MM-DD.log`) and improves debugging during automated pipeline runs.



## 🧠 **Design Principles**

| Principle        | Description                                          |
| ---------------- | ---------------------------------------------------- |
| **Reusability**  | Functions are modular and project-agnostic.          |
| **Traceability** | Logging ensures every read/write action is recorded. |
| **Consistency**  | Standard error interface via `CustomException`.      |
| **Reliability**  | Prevents silent failures in pipeline stages.         |

## 🚀 **Typical Usage in the Project**

Within the main training pipeline (`pipeline/training_pipeline.py`):

```python
from utils.common_functions import read_yaml, load_data
from config.paths_config import CONFIG_PATH

cfg = read_yaml(CONFIG_PATH)
train_df = load_data(cfg["data"]["train_path"])
```

This guarantees that all downstream steps (processing, feature engineering, model training) operate from consistent configuration sources.


## 🧾 **Module Summary**

| Function    | Input            | Output         | Raises            | Description                  |
| ----------- | ---------------- | -------------- | ----------------- | ---------------------------- |
| `read_yaml` | `file_path: str` | `dict`         | `CustomException` | Reads and parses YAML config |
| `load_data` | `csv_path: str`  | `pd.DataFrame` | `CustomException` | Loads dataset from CSV       |

## 🧩 **Integration Example (with Logger & Exception)**

```python
from utils.common_functions import read_yaml, load_data
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

try:
    cfg = read_yaml()
    df = load_data(cfg["data"]["train_path"])
except CustomException as e:
    logger.error(f"Pipeline halted: {e}")
```



## ✅ **Best Practices**

* Keep **`config.yaml`** under version control for reproducibility.
* Validate all file paths via `paths_config.py` to prevent runtime errors.
* Log every major I/O event to ensure observability during CI/CD pipeline runs.
* Avoid modifying these utilities directly — extend them if new I/O types are introduced.