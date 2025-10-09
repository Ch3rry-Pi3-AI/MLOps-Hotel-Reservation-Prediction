# 🗂️ `artifacts/` — Data & Model Artefacts

The `artifacts/` directory stores all **generated outputs** produced as the project progresses through its pipeline stages.
Each subfolder corresponds to a specific stage of the MLOps workflow — from raw data ingestion to processed datasets and trained model artefacts.

These files and folders are **created automatically** when you run the project’s various modules (e.g., `data_ingestion.py`, `data_preprocessing.py`, and `model_training.py`).

## 📁 Folder Structure

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

## 📦 Folder Descriptions

### 🧾 `raw/`

Contains the **original dataset** and **train/test splits** generated during the **data ingestion** stage.

| File        | Description                                                |
| :---------- | :--------------------------------------------------------- |
| `raw.csv`   | The complete dataset downloaded from Google Cloud Storage. |
| `train.csv` | The training portion of the dataset (typically 80%).       |
| `test.csv`  | The testing portion of the dataset (typically 20%).        |

### ⚙️ `processed/`

Stores **cleaned, encoded, balanced, and feature-selected datasets** created during the **data preprocessing** stage.

| File                  | Description                                                       |
| :-------------------- | :---------------------------------------------------------------- |
| `processed_train.csv` | The fully preprocessed training dataset ready for model training. |
| `processed_test.csv`  | The corresponding preprocessed test dataset for model evaluation. |

### 🧠 `models/`

Houses all **trained machine learning model artefacts** produced during the **model training** stage.

| File             | Description                                                                      |
| :--------------- | :------------------------------------------------------------------------------- |
| `lgbm_model.pkl` | The trained LightGBM model, saved in pickle format for inference and deployment. |

## 🔄 Notes

* These folders are **automatically created** by their respective modules — you don’t need to create them manually.
* Each file serves as an **intermediate or final output** for downstream stages in the MLOps pipeline.
* The folder structure ensures a clear, traceable flow of data from **raw ingestion → processing → model output**.

✅ **In summary:**
`artifacts/` is the **working directory of your MLOps project**, capturing the entire lifecycle of your dataset and model in a structured, reproducible way.
