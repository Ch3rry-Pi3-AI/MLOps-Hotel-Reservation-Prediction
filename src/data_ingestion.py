"""
data_ingestion.py
-----------------
Implements the DataIngestion class responsible for downloading
the hotel reservation dataset from Google Cloud Storage (GCS),
splitting it into train and test sets, and saving them locally.

This module integrates with:
- Centralised logging (src.logger)
- Custom exception handling (src.custom_exception)
- Configuration management (config/config.yaml and config/paths_config.py)

Usage
-----
Example:
    python src/data_ingestion.py

Notes
-----
- Requires GCP credentials to be set via the environment variable:
  GOOGLE_APPLICATION_CREDENTIALS
- Automatically creates necessary directories under `artifacts/raw/`
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard & Third-Party Imports
# -------------------------------------------------------------------
import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split

# -------------------------------------------------------------------
# Internal Imports
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

# -------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: DataIngestion
# -------------------------------------------------------------------
class DataIngestion:
    """
    Handles the ingestion of raw hotel reservation data from a GCP bucket.

    This includes:
    - Downloading the dataset from the configured GCP bucket.
    - Splitting the data into train and test subsets.
    - Saving the results into local CSV files for further processing.

    Parameters
    ----------
    config : dict
        Configuration dictionary loaded from `config/config.yaml`.
    """

    def __init__(self, config: dict):
        # Extract configuration parameters
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        # Ensure raw data directory exists
        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info(
            f"Data ingestion initialised with bucket '{self.bucket_name}' "
            f"and file '{self.file_name}'."
        )

    # -------------------------------------------------------------------
    # Method: download_csv_from_gcp
    # -------------------------------------------------------------------
    def download_csv_from_gcp(self) -> None:
        """
        Download the raw CSV dataset from Google Cloud Storage.

        The file is downloaded from the specified bucket and saved to
        `artifacts/raw/raw.csv`.

        Raises
        ------
        CustomException
            If any error occurs during the file download.
        """
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"CSV file successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("Error while downloading the CSV file.")
            import sys
            raise CustomException("Failed to download CSV file", sys) from e

    # -------------------------------------------------------------------
    # Method: split_data
    # -------------------------------------------------------------------
    def split_data(self) -> None:
        """
        Split the downloaded dataset into training and test sets
        based on the train/test ratio from configuration.

        Raises
        ------
        CustomException
            If any error occurs during the split or file writing process.
        """
        try:
            logger.info("Starting data split process.")

            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(
                data, test_size=1 - self.train_test_ratio, random_state=42
            )

            train_data.to_csv(TRAIN_FILE_PATH, index=False)
            test_data.to_csv(TEST_FILE_PATH, index=False)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("Error while splitting the dataset.")
            import sys
            raise CustomException("Failed to split data into train and test sets", sys) from e

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self) -> None:
        """
        Orchestrates the full data ingestion process:
        1. Downloads the raw dataset from GCP.
        2. Splits it into train/test sets.
        3. Logs the overall process.

        Notes
        -----
        - Custom exceptions are logged, but not re-raised.
        """
        try:
            logger.info("Starting data ingestion pipeline.")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion completed successfully.")

        except CustomException as ce:
            logger.error(f"CustomException: {str(ce)}")

        finally:
            logger.info("Data ingestion process completed.")


# -------------------------------------------------------------------
# Script Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()