"""
training_pipeline.py
----------------
Unified entrypoint for the full MLOps Hotel Reservation Prediction pipeline.

This script orchestrates the three major stages of the workflow:
  1. Data Ingestion
  2. Data Preprocessing
  3. Model Training

Each stage is modularised in `src/` and configured via `config/` YAML files.
Running this script executes the complete data-to-model process end-to-end.

Usage
-----
    python src/main_pipeline.py
"""

# -------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------
from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.paths_config import *


# -------------------------------------------------------------------
# Pipeline Orchestration
# -------------------------------------------------------------------
if __name__ == "__main__":

    # ===============================================================
    # 1️⃣  DATA INGESTION
    # ===============================================================
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

    # ===============================================================
    # 2️⃣  DATA PREPROCESSING
    # ===============================================================
    processor = DataProcessor(
        TRAIN_FILE_PATH,
        TEST_FILE_PATH,
        PROCESSED_DIR,
        CONFIG_PATH
    )
    processor.process()

    # ===============================================================
    # 3️⃣  MODEL TRAINING
    # ===============================================================
    trainer = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH,
        PROCESSED_TEST_DATA_PATH,
        MODEL_OUTPUT_PATH
    )
    trainer.run()