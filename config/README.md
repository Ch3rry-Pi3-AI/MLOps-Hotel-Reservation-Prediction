# 🧾 **Path Configuration — `paths_config.py`**

This module defines all **directory and file paths** used across the **MLOps Hotel Reservation Prediction** pipeline.
It ensures that every stage — from data ingestion to model training — writes and reads from a **consistent, version-controlled folder structure**.

All paths are relative to the project root and are **automatically created at runtime**, ensuring a clean, reproducible environment for data and artefact management.

## 📁 **File Overview**

```
mlops-hotel-reservation-prediction/
├── config/
│   └── paths_config.py
├── artifacts/
│   ├── raw/
│   │   ├── raw.csv
│   │   ├── train.csv
│   │   └── test.csv
│   ├── processed/
│   │   ├── processed_train.csv
│   │   └── processed_test.csv
│   └── models/
│       └── lgbm_model.pkl
```

## ⚙️ **Purpose**

The `paths_config.py` module standardises file path definitions across the project.
It eliminates hard-coded directory references within pipeline scripts, enabling clean imports and consistent directory management throughout the workflow.

## 🧩 **Key Sections**

| Section                | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| 🧾 **Data Ingestion**  | Defines storage locations for raw, train, and test datasets.               |
| 🧹 **Data Processing** | Stores processed (cleaned and feature-engineered) training and test files. |
| 🧠 **Model Training**  | Specifies where model artefacts such as `.pkl` files are saved.            |
| ⚙️ **Configuration**   | Provides the path to the main YAML configuration file (`config.yaml`).     |

## 🧠 **Example Usage**

```python
from config.paths_config import (
    RAW_FILE_PATH, TRAIN_FILE_PATH, TEST_FILE_PATH,
    PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH,
    MODEL_OUTPUT_PATH, CONFIG_PATH
)
```

## ✅ **Summary**

| Variable                                                | Description                                           |
| ------------------------------------------------------- | ----------------------------------------------------- |
| `RAW_FILE_PATH`, `TRAIN_FILE_PATH`, `TEST_FILE_PATH`    | Raw and split dataset paths.                          |
| `PROCESSED_TRAIN_DATA_PATH`, `PROCESSED_TEST_DATA_PATH` | Cleaned and processed dataset paths.                  |
| `MODEL_OUTPUT_PATH`                                     | Directory for model artefacts (e.g. LightGBM `.pkl`). |
| `CONFIG_PATH`                                           | Path to the main configuration file (`config.yaml`).  |

## 🧩 **Design Highlights**

* **Single Source of Truth:** All pipeline stages import consistent file paths from one place.
* **Automatic Directory Creation:** Ensures folder hierarchy exists before writing outputs.
* **Reproducibility:** Enables predictable and structured artefact storage for each run.
* **Portability:** Works seamlessly across local and cloud environments.