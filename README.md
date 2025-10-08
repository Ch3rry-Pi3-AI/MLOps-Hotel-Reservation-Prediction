# 🏗️ **Initial Project Setup — MLOps Hotel Reservation Prediction**

This branch establishes the **foundational structure** for the **MLOps Hotel Reservation Prediction** project.
It sets up a modular Python package under `src/`, adds **logging** and **custom exception handling**, and prepares the repository for subsequent MLOps pipeline stages.



## 🗂️ **Project Structure**

```
mlops-hotel-reservation-prediction/
├── artifacts/                                      # 📦 Model artefacts and outputs
├── config/                                         # ⚙️ Configuration modules for pipeline stages
│   ├── __init__.py
├── MLOps_Hotel_Reservation_Prediction.egg-info/    # 📁 Auto-generated package metadata
├── notebook/                                       # 📓 Jupyter notebooks for exploration and testing
├── pipeline/                                       # 🔄 Future pipeline orchestration modules
│   ├── __init__.py
├── src/                                            # 🧠 Core source package
│   ├── __init__.py
│   ├── custom_exception.py                         #   Custom exception class with file/line context
│   └── logger.py                                   #   Centralised daily logging configuration
├── static/                                         # 🧱 Static assets (images, configuration examples)
├── templates/                                      # 🪶 Templates for documentation or deployment
├── utils/                                          # 🧰 Utility functions (helper scripts and shared logic)
│   ├── __init__.py
├── .gitignore                                      # 🚫 Git ignore rules
├── README.md                                       # 📖 Project documentation (you are here)
├── requirements.txt                                # 📦 Python dependencies
├── setup.py                                        # ⚙️ Package metadata and configuration
└── venv/                                           # 🧩 Local virtual environment (ignored in Git)
```

> 💡 **Note:** The `venv/` directory is ignored by Git and should not be committed.



## ⚙️ **Setup Process**

The following steps outline how this foundational setup was created.

### **1️⃣ Create the Project Structure**

Directories were created to separate **source code**, **configuration**, **utilities**, and **artefacts**.
Empty directories were initialised with `README.md` files for visibility and Git tracking.



### **2️⃣ Create and Activate the Virtual Environment**

A new Python environment was created using the built-in `venv` module:

```bash
python -m venv venv
```

Activate the environment (Windows Command Prompt):

```bash
venv\Scripts\activate
```

Once activated, `(venv)` will appear in the terminal prompt.



### **3️⃣ Create the `requirements.txt` File**

A minimal dependencies list was defined to support the base setup.
This file will expand in later branches as new functionality is added.

Example:

```text
pandas
numpy
scikit-learn
```

Install all dependencies:

```bash
pip install -r requirements.txt
```



### **4️⃣ Create the `setup.py` File**

A `setup.py` was created at the root to make the repository installable as a Python package.

```python
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MLOPS-Hotel-Reservation-Prediction",
    version="0.1",
    author="Ch3rry Pi3",
    packages=find_packages(),
    install_requires=requirements,
)
```

Install the package in editable mode:

```bash
pip install -e .
```

This enables absolute imports such as:

```python
from src.logger import get_logger
from src.custom_exception import CustomException
```



### **5️⃣ Add Core Source Modules**

Two key utility modules were created within `src/` to standardise logging and exception handling.

| File                  | Description                                                                           |
|  | - |
| `logger.py`           | Defines a central logging setup with date-based log files and INFO-level logging.     |
| `custom_exception.py` | Custom exception class that captures filename and line number for detailed debugging. |



## 🚀 **Next Steps**

In the next branch (`01_data_ingestion`), we will ingest the project data from a Google Cloud Platform (GCP) bucket!
