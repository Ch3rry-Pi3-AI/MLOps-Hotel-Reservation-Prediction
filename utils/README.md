# 🧰 **Utility Module — `common_functions.py`**

This module provides a **shared configuration utility** for the **MLOps Anime Recommender System** project.
It standardises how YAML configuration files are read and validated, ensuring that all pipeline components access project settings in a **consistent, traceable, and error-resilient** manner.

## 🗂️ **File Location**

```
mlops-anime-recommender-system/
├── src/
│   ├── logger.py
│   ├── custom_exception.py
├── config/
│   ├── paths_config.py
│   └── config.yaml
└── utils/
    └── common_functions.py   # 🧰 Shared YAML configuration utility
```


## 🎯 **Purpose**

The `common_functions.py` module centralises the **YAML configuration handling** used across the entire pipeline.
Its single utility function, `read_yaml()`, reads and parses configuration files like `config/config.yaml` and integrates tightly with the project’s logging and exception systems.

| Function      | Description                                                  |
| ------------- | ------------------------------------------------------------ |
| `read_yaml()` | Reads and parses YAML configuration files into Python dicts. |

This design supports **reproducibility**, **consistent configuration management**, and **clear error handling** across all pipeline modules (e.g., `data_ingestion.py`, `training_pipeline.py`).

## ⚙️ **Dependencies**

| Type                 | Modules Used                                                |
| -------------------- | ----------------------------------------------------------- |
| **Standard Library** | `os`, `sys`                                                 |
| **Third-Party**      | `yaml`                                                      |
| **Internal**         | `src.logger`, `src.custom_exception`, `config.paths_config` |

## 🔧 **Function Overview**

### 1️⃣ `read_yaml(file_path: str = CONFIG_PATH) -> dict`

Reads and validates a YAML configuration file (defaults to `config/config.yaml`) and returns a dictionary of configuration parameters.

**Example:**

```python
from utils.common_functions import read_yaml

cfg = read_yaml()
print(cfg["data"]["train_path"])
```

**Key Features:**

* Automatically loads configuration from the path defined in `CONFIG_PATH`.
* Logs successful reads with timestamps.
* Raises `CustomException` for missing, inaccessible, or invalid files.
* Uses `yaml.safe_load()` for secure parsing.

**Example Log:**

```text
INFO - Successfully read YAML config: config/config.yaml
```


## 🧱 **Error Handling & Logging**

All exceptions are managed using:

* `src/logger.get_logger()` — unified logging for all modules.
* `src/custom_exception.CustomException` — wraps raw exceptions with detailed context.

**Example Log:**

```text
ERROR - Error while reading YAML file 'config/missing.yaml': File not found
```

This ensures visibility into configuration issues during both local runs and automated CI/CD executions.


## 🧠 **Design Principles**

| Principle        | Description                                       |
| ---------------- | ------------------------------------------------- |
| **Simplicity**   | Keeps configuration handling focused and minimal. |
| **Reusability**  | Provides a single, central access point for YAML. |
| **Traceability** | Every config read is logged for reproducibility.  |
| **Reliability**  | Prevents silent failures in pipeline operations.  |


## 🚀 **Example Integration**

Within the main training pipeline (`pipeline/training_pipeline.py`):

```python
from utils.common_functions import read_yaml
from config.paths_config import CONFIG_PATH

cfg = read_yaml(CONFIG_PATH)
print(cfg["data"]["anime_path"])
```

This ensures all modules in the Anime Recommender pipeline reference the same configuration structure, maintaining project-wide consistency.


## 🧾 **Module Summary**

| Function    | Input            | Output | Raises            | Description                  |
| ----------- | ---------------- | ------ | ----------------- | ---------------------------- |
| `read_yaml` | `file_path: str` | `dict` | `CustomException` | Reads and parses YAML config |

## ✅ **Best Practices**

* Keep `config.yaml` under version control for full experiment reproducibility.
* Validate and centralise all file paths in `paths_config.py`.
* Log every configuration load event for clear CI/CD observability.
* Extend this module only if additional configuration formats (e.g. JSON) are introduced.

