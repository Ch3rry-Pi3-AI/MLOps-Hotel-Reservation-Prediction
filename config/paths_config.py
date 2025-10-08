"""
paths_config.py
---------------
Centralised file path configuration for the MLOps Hotel Reservation Prediction project.

This module defines key directory and file paths used throughout the pipeline,
including raw data, processed data, and model artefacts.

Usage
-----
Example:
    from config.paths_config import RAW_FILE_PATH, CONFIG_PATH

Notes
-----
- All paths are defined relative to the project root.
- Directories are created dynamically where necessary.
"""

import os

# -------------------------------------------------------------------
# 🧾 DATA INGESTION
# -------------------------------------------------------------------
RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = "config/config.yaml"