# 🧱 `src/` — Core Utility Modules

This directory contains two foundational modules that establish **error handling** and **logging standards** across the MLOps Hotel Reservation Prediction project.
They ensure that all scripts (data ingestion, preprocessing, training, etc.) follow **consistent, traceable, and maintainable debugging practices**.

## ⚠️ `custom_exception.py`

Defines a **Custom Exception Class** that enriches error messages with contextual information — including the file name and line number where the issue occurred.

### 📋 **Overview**

| Aspect          | Description                                                                               |
| :-------------- | :---------------------------------------------------------------------------------------- |
| **Purpose**     | To provide a unified and descriptive error handling mechanism across all pipeline stages. |
| **Key Feature** | Automatically extracts and appends file name and line number to the exception message.    |
| **Integration** | Used across all modules to wrap unexpected errors with clear tracebacks.                  |

### 🧩 **Usage Example**

```python
from src.custom_exception import CustomException
import sys

try:
    result = 10 / 0
except Exception as e:
    raise CustomException(str(e), sys)
```

### 🧠 **Notes**

* All raised exceptions will display a **detailed message** like:
  `Error in src/data_ingestion.py, line 42: division by zero`
* Use this class whenever you need consistent, informative exceptions for debugging or logging.

## 🧾 `logger.py`

Provides a **centralised logging configuration** for the entire project.
Each log message is timestamped, categorised by severity, and stored in a **daily rotating log file** located under the `logs/` directory.

### 📋 **Overview**

| Aspect            | Description                                                                                     |
| :---------------- | :---------------------------------------------------------------------------------------------- |
| **Purpose**       | To standardise log messages across all modules and automatically write them to dated log files. |
| **Log Directory** | `logs/` — automatically created if it doesn’t exist.                                            |
| **File Format**   | `log_YYYY-MM-DD.log` (one file per day).                                                        |
| **Default Level** | INFO                                                                                            |
| **Log Format**    | `timestamp - level - message`                                                                   |

### 🧩 **Usage Example**

```python
from src.logger import get_logger

logger = get_logger(__name__)
logger.info("Data ingestion started.")
logger.error("Failed to connect to data source.")
```

### 🧠 **Notes**

* Ideal for tracing pipeline progress across ingestion, preprocessing, and training stages.
* All logs are stored persistently in the `logs/` folder for easy review.
* Integrates seamlessly with `CustomException` for traceable debugging.

### ✅ **Summary**

| Module                | Purpose                   | Typical Use Case                          |
| :-------------------- | :------------------------ | :---------------------------------------- |
| `custom_exception.py` | Consistent error handling | Wraps exceptions in any pipeline stage    |
| `logger.py`           | Centralised logging       | Tracks progress and errors across scripts |

Together, these two modules form the **diagnostic backbone** of the MLOps pipeline — ensuring that every process step is traceable, well-documented, and easy to debug.
