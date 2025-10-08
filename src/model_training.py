"""
model_training.py
-----------------
Model training module for the MLOps Hotel Reservation Prediction project.

This script implements a complete training pipeline using **LightGBM** with
hyperparameter optimisation via **RandomizedSearchCV**, integrated with **MLflow**
for experiment tracking and reproducibility.

The process includes:
  1) Loading and splitting processed data
  2) Hyperparameter tuning with RandomizedSearchCV
  3) Model evaluation using standard classification metrics
  4) Saving the trained model artefact
  5) Logging artefacts, parameters, and metrics to MLflow

Usage
-----
Example:
    from config.paths_config import *
    from src.model_training import ModelTraining

    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    trainer.run()

Notes
-----
- Depends on preprocessed data generated from `src/data_preprocessing.py`
- Produces `artifacts/models/lgbm_model.pkl`
- Logs experiments via MLflow for full traceability
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import os

# -------------------------------------------------------------------
# Core Data & ML Libraries
# -------------------------------------------------------------------
import pandas as pd
import joblib
import lightgbm as lgb
from scipy.stats import randint
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# -------------------------------------------------------------------
# Project Utilities & Config
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data

# -------------------------------------------------------------------
# Experiment Tracking
# -------------------------------------------------------------------
import mlflow
import mlflow.sklearn

# -------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Class: ModelTraining
# -------------------------------------------------------------------
class ModelTraining:
    """
    Orchestrates the full model training pipeline using LightGBM.

    Parameters
    ----------
    train_path : str
        Path to the preprocessed training dataset.
    test_path : str
        Path to the preprocessed test dataset.
    model_output_path : str
        Destination path for the trained model pickle file.
    """

    def __init__(self, train_path: str, test_path: str, model_output_path: str):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        # Load parameter spaces from config
        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    # -------------------------------------------------------------------
    # Method: load_and_split_data
    # -------------------------------------------------------------------
    def load_and_split_data(self):
        """
        Loads processed train/test data and splits them into features and target.

        Returns
        -------
        tuple
            X_train, y_train, X_test, y_test
        """
        try:
            logger.info(f"Loading training data from: {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading test data from: {self.test_path}")
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data successfully split for model training.")
            return X_train, y_train, X_test, y_test

        except Exception as e:
            logger.error(f"Error while loading data: {e}")
            raise CustomException("Failed to load and split data", e)

    # -------------------------------------------------------------------
    # Method: train_lgbm
    # -------------------------------------------------------------------
    def train_lgbm(self, X_train, y_train):
        """
        Trains a LightGBM classifier using RandomizedSearchCV for hyperparameter tuning.

        Returns
        -------
        lgb.LGBMClassifier
            The best-performing LightGBM model found during random search.
        """
        try:
            logger.info("Initialising LightGBM model.")
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])

            logger.info("Starting hyperparameter tuning with RandomizedSearchCV.")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                random_state=self.random_search_params["random_state"],
                scoring=self.random_search_params["scoring"]
            )

            random_search.fit(X_train, y_train)

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info("Hyperparameter tuning completed successfully.")
            logger.info(f"Best parameters: {best_params}")

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error while training model: {e}")
            raise CustomException("Failed to train LightGBM model", e)

    # -------------------------------------------------------------------
    # Method: evaluate_model
    # -------------------------------------------------------------------
    def evaluate_model(self, model, X_test, y_test):
        """
        Evaluates the trained model on the test dataset.

        Returns
        -------
        dict
            Dictionary containing accuracy, precision, recall, and F1 score.
        """
        try:
            logger.info("Evaluating trained model performance.")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            logger.info(f"Accuracy Score  : {accuracy:.4f}")
            logger.info(f"Precision Score : {precision:.4f}")
            logger.info(f"Recall Score    : {recall:.4f}")
            logger.info(f"F1 Score        : {f1:.4f}")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }

        except Exception as e:
            logger.error(f"Error while evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)

    # -------------------------------------------------------------------
    # Method: save_model
    # -------------------------------------------------------------------
    def save_model(self, model):
        """
        Saves the trained model to disk using joblib.

        Parameters
        ----------
        model : object
            Trained model to be saved.
        """
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving trained model to disk.")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model successfully saved to: {self.model_output_path}")

        except Exception as e:
            logger.error(f"Error while saving model: {e}")
            raise CustomException("Failed to save trained model", e)

    # -------------------------------------------------------------------
    # Method: run
    # -------------------------------------------------------------------
    def run(self):
        """
        Executes the full model training pipeline with MLflow integration.
        """
        try:
            with mlflow.start_run():
                logger.info("🚀 Starting Model Training Pipeline")
                logger.info("Initialising MLflow experiment tracking.")

                # Log training and test datasets as artefacts
                logger.info("Logging datasets to MLflow.")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")
                mlflow.log_artifact(self.test_path, artifact_path="datasets")

                # Load, train, and evaluate
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)

                # Log model and metrics
                logger.info("Logging trained model and metrics to MLflow.")
                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("✅ Model training pipeline completed successfully.")

        except Exception as e:
            logger.error(f"Error in model training pipeline: {e}")
            raise CustomException("Failed during model training pipeline", e)


# -------------------------------------------------------------------
# Script Entrypoint
# -------------------------------------------------------------------
if __name__ == "__main__":
    trainer = ModelTraining(
        PROCESSED_TRAIN_DATA_PATH,
        PROCESSED_TEST_DATA_PATH,
        MODEL_OUTPUT_PATH
    )
    trainer.run()