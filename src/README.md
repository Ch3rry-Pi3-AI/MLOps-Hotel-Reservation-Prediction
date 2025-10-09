# 🧩 **Source Code Directory — `src/`**

This directory contains all **core Python modules** that define the functional backbone of the **MLOps Hotel Reservation Prediction** pipeline.
Each module performs a specific task — such as logging, data ingestion, or error handling — while following consistent configuration and exception patterns.

The `src/` folder ensures a clear separation between **code**, **configuration**, and **artifacts**, promoting modularity, scalability, and ease of maintenance across all stages of the project.

## 📁 **Folder Structure**

```
mlops-hotel-reservation-prediction/
├── src/
│   ├── custom_exception.py      # Unified exception handling
│   ├── data_ingestion.py        # Downloads and splits raw data from GCP
│   └── logger.py                # Centralised logging configuration
```

## 🎯 **Overview of Modules**

### 🧱 `logger.py`

Centralised logging configuration for the entire project.
It automatically creates daily log files under the `logs/` directory and timestamps each message for traceability.

**Key Features**

* Configures global `INFO`-level logging
* Stores logs in `logs/log_YYYY-MM-DD.log`
* Provides a helper function `get_logger(name)` for consistent logging across all modules

**Example**

```python
from src.logger import get_logger

logger = get_logger(__name__)
logger.info("Data ingestion started.")
```

---

### ⚠️ `custom_exception.py`

Defines the `CustomException` class for unified and descriptive error handling.
Each raised exception automatically includes the **file name** and **line number** of the error, making debugging faster and clearer.

**Key Features**

* Wraps raw Python exceptions with contextual details
* Integrates seamlessly with the global logger
* Provides consistent error messages across the pipeline

**Example**

```python
try:
    result = 10 / 0
except Exception as e:
    import sys
    raise CustomException(str(e), sys)
```

---

### ☁️ `data_ingestion.py`

Implements the `DataIngestion` class responsible for **downloading** the dataset from **Google Cloud Storage (GCS)**,
**splitting** it into training and testing subsets, and **saving** them under `artifacts/raw/`.

**Key Steps**

1. Connects to GCS using the `google-cloud-storage` client
2. Downloads the raw dataset defined in `config/config.yaml`
3. Splits the dataset into training and testing sets based on the configured ratio
4. Logs all operations and stores outputs locally

**Example**

```python
from utils.common_functions import read_yaml
from config.paths_config import CONFIG_PATH
from src.data_ingestion import DataIngestion

cfg = read_yaml(CONFIG_PATH)
data_ingestion = DataIngestion(cfg)
data_ingestion.run()
```

**Outputs**

* `artifacts/raw/raw.csv`
* `artifacts/raw/train.csv`
* `artifacts/raw/test.csv`

---

## 🧠 **Design Principles**

* **Separation of Concerns:** Each module handles a single, well-defined task
* **Reusability:** All classes can be imported and executed independently
* **Consistency:** Unified logging, exception handling, and configuration access
* **Traceability:** Each stage logs operations with timestamps and contextual messages
* **Pipeline Integration:** Designed for seamless execution within CI/CD systems such as Jenkins or GitHub Actions

## ✅ **Summary**

| Module                | Responsibility                         | Key Output                    |
| --------------------- | -------------------------------------- | ----------------------------- |
| `logger.py`           | Centralised logging configuration      | Daily log files under `logs/` |
| `custom_exception.py` | Unified, contextual exception handling | Traceable error messages      |
| `data_ingestion.py`   | GCP data download and train/test split | `train.csv`, `test.csv`       |