Perfect 👍 — here’s the **fully updated README** for your **Data Preprocessing stage**, now including the “How to Run” section and preserving your established formatting and tone.

---

# ⚙️ **Data Preprocessing — MLOps Hotel Reservation Prediction**

This branch marks the transition from **notebook experimentation** to a **modular, reproducible data preprocessing pipeline**.
Following the insights gained during the **Exploratory Analysis** stage, the data scientist’s workflow has now been **refactored into Python scripts** that can be reused, parameterised, and integrated into the full MLOps pipeline.

The goal of this stage is to **automate the cleaning, encoding, transformation, and feature selection process** used in the notebook — establishing a solid, repeatable foundation for model training in the next stage.

## 🧾 **What’s New in This Stage**

This branch introduces several key updates and new modules:

* 🆕 **`src/data_preprocessing.py`** — a fully modular script encapsulating all data cleaning, encoding, class balancing, and feature selection logic within a single `DataProcessor` class.
  This design was made possible thanks to experimentation and validation in the previous notebook stage.
* 🔧 **`config/config.yaml`** — updated to include configurable parameters for categorical/numerical columns, skewness threshold, and number of features to select.
* 🗺️ **`config/paths_config.py`** — updated to define new paths for processed outputs (`PROCESSED_TRAIN_DATA_PATH`, `PROCESSED_TEST_DATA_PATH`).
* 🧰 **`utils/common_functions.py`** — extended with helper utilities such as `read_yaml()` and `load_data()` for consistent data access across modules.
* 📦 **New output folder:** `artifacts/processed/` — automatically created by the preprocessing pipeline to store `processed_train.csv` and `processed_test.csv`.

## 🧩 **Key Functionalities**

The new `DataProcessor` class performs the following steps end-to-end:

1. **Data Cleaning** — drops unnecessary columns (`Unnamed: 0`, `Booking_ID`) and duplicates.
2. **Categorical Encoding** — applies label encoding to categorical columns defined in YAML.
3. **Skewness Handling** — uses `np.log1p()` to transform highly skewed numeric features.
4. **Class Balancing** — applies **SMOTE** to mitigate booking status imbalance.
5. **Feature Selection** — selects top-N important features using a `RandomForestClassifier`.
6. **Data Saving** — writes the cleaned and balanced datasets to the new `artifacts/processed/` directory.

Each transformation step is logged using the centralised project logger and wrapped with a custom exception handler for traceable debugging.

## 🧠 **How to Run the Pipeline**

After activating your virtual environment and installing dependencies:

```bash
python src/data_preprocessing.py
```

This command executes the full preprocessing workflow:

* Loads raw training and test data from `artifacts/raw/`
* Applies cleaning, encoding, balancing, and feature selection
* Saves processed outputs to `artifacts/processed/processed_train.csv` and `processed_test.csv`

## 🗂️ **Updated Project Structure**

```
mlops-hotel-reservation-prediction/
├── artifacts/
│   ├── raw/                             # From previous ingestion stage
│   │   ├── raw.csv
│   │   ├── train.csv
│   │   └── test.csv
│   └── processed/                       # 🆕 Newly created by this stage
│       ├── processed_train.csv
│       └── processed_test.csv
├── config/
│   ├── config.yaml                      # 🔧 Updated with preprocessing params
│   └── paths_config.py                  # 🔧 Updated with processed paths
├── src/
│   ├── data_ingestion.py
│   ├── data_preprocessing.py            # 🆕 Main preprocessing pipeline module
│   ├── logger.py
│   ├── custom_exception.py
│   └── __init__.py
├── utils/
│   └── common_functions.py              # 🔧 Extended helper functions
├── notebooks/
│   └── notebook.ipynb                   # From previous EDA stage
├── requirements.txt
├── setup.py
└── README.md                            # 📖 You are here
```

## 🔍 **Pipeline Highlights**

Within `src/data_preprocessing.py`, the `DataProcessor` class:

* Loads raw CSVs from `artifacts/raw/`
* Applies consistent, YAML-driven transformations
* Balances and filters features automatically
* Saves the processed outputs ready for model training

The pipeline ensures **reproducibility**, **traceability**, and **config-driven control**, setting the foundation for scalable MLOps automation.

## 🚀 **Next Stage — Model Training**

In the next branch, the project evolves into a **Model Training** stage, where the processed data will feed into a modular training pipeline that:

* Loads preprocessed data from `artifacts/processed/`
* Trains, evaluates, and saves machine learning models
* Logs experiments to **MLflow** for versioning and reproducibility
* Prepares models for downstream **inference and deployment**

This stage completes the transformation from **raw data → clean, ready-to-train datasets**, paving the way for **automated model experimentation and evaluation** in the next phase.