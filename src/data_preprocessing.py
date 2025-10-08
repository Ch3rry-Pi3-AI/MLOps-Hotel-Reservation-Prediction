"""
data_preprocessing.py
---------------------
Data preprocessing module for the MLOps Hotel Reservation Prediction project.

This script encapsulates the data scientist's notebook workflow into a
single class, `DataProcessor`, that:
  1) Cleans raw inputs (drop columns/duplicates)
  2) Encodes categoricals (Label Encoding)
  3) Handles skewness (log1p based on a configurable threshold)
  4) Balances classes via SMOTE
  5) Selects top-N features using a RandomForestClassifier
  6) Saves processed train/test outputs

Configuration is driven by `config/config.yaml` and centralised paths in
`config/paths_config.py`. Logging uses the shared project logger.

Usage
-----
Example:
    from config.paths_config import *
    from src.data_preprocessing import DataProcessor

    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

Notes
-----
- Logic is intentionally preserved from the notebook/code-behind version.
- Output files are written under `artifacts/processed/`.
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import os

# -------------------------------------------------------------------
# Core Data Analysis & Manipulation
# -------------------------------------------------------------------
import pandas as pd
import numpy as np

# -------------------------------------------------------------------
# Project Utilities & Config
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data

# -------------------------------------------------------------------
# ML Tooling
# -------------------------------------------------------------------
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# -------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: DataProcessor
# -------------------------------------------------------------------
class DataProcessor:
    """
    Orchestrates preprocessing steps for train and test data.

    Parameters
    ----------
    train_path : str
        Path to the raw training CSV.
    test_path : str
        Path to the raw test CSV.
    processed_dir : str
        Directory where processed outputs will be saved.
    config_path : str
        Path to the YAML configuration file.
    """

    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    # -------------------------------------------------------------------
    # Method: preprocess_data
    # -------------------------------------------------------------------
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply base cleaning, label encoding, and skewness handling.

        Steps
        -----
        - Drop 'Unnamed: 0' and 'Booking_ID' if present
        - Drop duplicate rows
        - Label encode categorical columns (mapping logged)
        - Apply log1p to numeric columns over skewness threshold

        Returns
        -------
        pd.DataFrame
            Preprocessed DataFrame.
        """
        try:
            logger.info("Starting our Data Processing step")

            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying Label Encoding")
            label_encoder = LabelEncoder()
            mappings = {}

            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {
                    label: code
                    for label, code in zip(
                        label_encoder.classes_,
                        label_encoder.transform(label_encoder.classes_)
                    )
                }

            logger.info("Label Mappings are : ")
            for col, mapping in mappings.items():
                logger.info(f"{col} : {mapping}")

            logger.info("Doing Skewness HAndling")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness = df[num_cols].apply(lambda x: x.skew())

            for column in skewness[skewness > skew_threshold].index:
                df[column] = np.log1p(df[column])

            return df

        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error while preprocess data", e)

    # -------------------------------------------------------------------
    # Method: balance_data
    # -------------------------------------------------------------------
    def balance_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Balance the dataset using SMOTE.

        Returns
        -------
        pd.DataFrame
            Balanced DataFrame with original column names and target.
        """
        try:
            logger.info("Handling Imbalanced Data")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced sucesffuly")
            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing data step {e}")
            raise CustomException("Error while balancing data", e)

    # -------------------------------------------------------------------
    # Method: select_features
    # -------------------------------------------------------------------
    def select_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select top-N features using RandomForest feature importance.

        Returns
        -------
        pd.DataFrame
            DataFrame restricted to top-N features plus the target.
        """
        try:
            logger.info("Starting our Feature selection step")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            })
            top_features_importance_df = feature_importance_df.sort_values(
                by="importance", ascending=False
            )

            num_features_to_select = self.config["data_processing"]["no_of_features"]
            top_10_features = top_features_importance_df["feature"].head(
                num_features_to_select
            ).values

            logger.info(f"Features selected : {top_10_features}")

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature slection completed sucesfully")
            return top_10_df

        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error while feature selection", e)

    # -------------------------------------------------------------------
    # Method: save_data
    # -------------------------------------------------------------------
    def save_data(self, df: pd.DataFrame, file_path: str) -> None:
        """
        Save a DataFrame to CSV.

        Parameters
        ----------
        df : pd.DataFrame
            Data to save.
        file_path : str
            Output CSV path.
        """
        try:
            logger.info("Saving our data in processed folder")
            df.to_csv(file_path, index=False)
            logger.info(f"Data saved sucesfuly to {file_path}")

        except Exception as e:
            logger.error(f"Error during saving data step {e}")
            raise CustomException("Error while saving data", e)

    # -------------------------------------------------------------------
    # Method: process
    # -------------------------------------------------------------------
    def process(self) -> None:
        """
        Run the end-to-end preprocessing pipeline:
        - Load raw train/test
        - Preprocess (clean, encode, skewness)
        - Balance (SMOTE)
        - Select top-N features
        - Save processed outputs
        """
        try:
            logger.info("Loading data from RAW directory")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed sucesfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline {e}")
            raise CustomException("Error while data preprocessing pipeline", e)


# -------------------------------------------------------------------
# Script Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()