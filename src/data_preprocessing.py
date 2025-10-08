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
            logger.info("Starting data processing step")

            # --- Drop columns only if present (prevents KeyError) ---
            to_consider = ['Unnamed: 0', 'Booking_ID']
            cols_to_drop = [c for c in to_consider if c in df.columns]
            if cols_to_drop:
                logger.info(f"Dropping columns: {cols_to_drop}")
                df = df.drop(columns=cols_to_drop)

            # --- Drop duplicates ---
            before = len(df)
            df = df.drop_duplicates()
            after = len(df)
            if before != after:
                logger.info(f"Dropped {before - after} duplicate rows")

            # --- Columns from config (intersect with df to be safe) ---
            cfg_cat = self.config["data_processing"]["categorical_columns"]
            cfg_num = self.config["data_processing"]["numerical_columns"]
            cat_cols = [c for c in cfg_cat if c in df.columns]
            num_cols = [c for c in cfg_num if c in df.columns]

            # --- Label Encoding (robust to NaNs and unexpected types) ---
            logger.info("Applying Label Encoding")
            mappings = {}
            for col in cat_cols:
                le = LabelEncoder()
                # Cast to string and fill NaN consistently to avoid errors
                series = df[col].astype(str).fillna("NA_CATEGORY")
                df[col] = le.fit_transform(series)
                mappings[col] = {
                    label: code
                    for label, code in zip(
                        le.classes_,
                        le.transform(le.classes_)
                    )
                }

            if mappings:
                logger.info("Label mappings:")
                for col, mapping in mappings.items():
                    logger.info(f"{col}: {mapping}")

            # --- Skewness Handling (only on numeric present) ---
            logger.info("Handling skewness")
            skew_threshold = self.config["data_processing"]["skewness_threshold"]

            # Ensure numeric dtype (coerce where needed)
            for c in num_cols:
                df[c] = pd.to_numeric(df[c], errors="coerce")

            skewness = df[num_cols].apply(lambda x: x.skew(skipna=True)) if num_cols else pd.Series(dtype=float)
            high_skew_cols = skewness[skewness > skew_threshold].index.tolist()

            for column in high_skew_cols:
                # log1p safe on non-negative; if negatives exist, shift
                col_min = df[column].min(skipna=True)
                if pd.notna(col_min) and col_min < 0:
                    shift = abs(col_min) + 1.0
                    df[column] = np.log1p(df[column] + shift)
                else:
                    df[column] = np.log1p(df[column])

            return df

        except Exception as e:
            logger.error(f"Error during preprocess step: {e}")
            raise CustomException("Error while preprocessing data", e)

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
            logger.info("Handling imbalanced data with SMOTE")

            if "booking_status" not in df.columns:
                raise ValueError("Target column 'booking_status' not found in DataFrame.")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            # Log basic class distribution
            y_counts = y.value_counts(dropna=False).to_dict()
            logger.info(f"Class distribution before SMOTE: {y_counts}")

            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
            balanced_df["booking_status"] = y_resampled

            logger.info("Data balanced successfully")
            return balanced_df

        except Exception as e:
            logger.error(f"Error during balancing data step: {e}")
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
            logger.info("Starting feature selection step")

            if "booking_status" not in df.columns:
                raise ValueError("Target column 'booking_status' not found in DataFrame.")

            X = df.drop(columns='booking_status')
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'feature': X.columns,
                'importance': feature_importance
            }).sort_values(by="importance", ascending=False)

            num_features_to_select = int(self.config["data_processing"]["no_of_features"])
            num_features_to_select = max(1, min(num_features_to_select, X.shape[1]))

            top_features = feature_importance_df["feature"].head(num_features_to_select).tolist()
            logger.info(f"Features selected: {top_features}")

            selected_df = df[top_features + ["booking_status"]]

            logger.info("Feature selection completed successfully")
            return selected_df

        except Exception as e:
            logger.error(f"Error during feature selection step: {e}")
            raise CustomException("Error during feature selection", e)

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
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            logger.info(f"Saving processed data to: {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Data saved successfully")

        except Exception as e:
            logger.error(f"Error during saving data step: {e}")
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

            # NOTE: Typically we do NOT apply SMOTE to the test set.
            # Kept here to preserve original logic, as per module notes.
            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)

            # Align test columns to selected train features (order & presence)
            test_df = test_df.reindex(columns=train_df.columns, fill_value=0)

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline: {e}")
            raise CustomException("Error during data preprocessing pipeline", e)


# -------------------------------------------------------------------
# Script Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()
