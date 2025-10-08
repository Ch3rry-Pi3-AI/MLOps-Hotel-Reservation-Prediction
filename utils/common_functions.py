"""
common_functions.py
-------------------
Shared utility functions for configuration loading and dataset IO.

This module provides:
1) `read_yaml` - reads YAML configuration (defaults to `config/config.yaml`).
2) `load_data` - loads CSV datasets into pandas DataFrames.

The functions integrate with the project-wide logger and raise
`CustomException` for consistent, descriptive error handling.

Usage
-----
Example:
    from utils.common_functions import read_yaml, load_data

    cfg = read_yaml()  # uses CONFIG_PATH from config/paths_config.py
    df  = load_data("artifacts/raw/train.csv")

Notes
-----
- Default YAML path is imported from `config.paths_config.CONFIG_PATH`.
- Errors are logged and re-raised as `CustomException`.
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import os

# -------------------------------------------------------------------
# Third-Party Imports
# -------------------------------------------------------------------
import yaml
import pandas as pd

# -------------------------------------------------------------------
# Internal Imports
# -------------------------------------------------------------------
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import CONFIG_PATH 

# -------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------
logger = get_logger(__name__)


# -------------------------------------------------------------------
# Function: read_yaml
# -------------------------------------------------------------------
def read_yaml(file_path: str = CONFIG_PATH) -> dict:
    """
    Read a YAML configuration file and return its contents as a dictionary.

    Parameters
    ----------
    file_path : str, optional
        Path to the YAML file. Defaults to `CONFIG_PATH` from
        `config.paths_config`.

    Returns
    -------
    dict
        Parsed YAML contents.

    Raises
    ------
    CustomException
        If the file does not exist or cannot be parsed.
    """
    try:
        # Validate file existence
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found at path: {file_path}")

        # Read YAML with UTF-8 encoding
        with open(file_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
            logger.info(f"Successfully read YAML config: {file_path}")
            return cfg

    except Exception as e:
        logger.error(f"Error while reading YAML file '{file_path}': {e}")
        import sys
        raise CustomException("Failed to read YAML configuration", sys) from e


# -------------------------------------------------------------------
# Function: load_data
# -------------------------------------------------------------------
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.

    Returns
    -------
    pandas.DataFrame
        The loaded dataset.

    Raises
    ------
    CustomException
        If the CSV cannot be read or parsed.
    """
    try:
        logger.info(f"Loading data from: {csv_path}")
        df = pd.read_csv(csv_path)
        logger.info(f"Data loaded successfully: shape={df.shape}")
        return df

    except Exception as e:
        logger.error(f"Error while loading data from '{csv_path}': {e}")
        import sys
        raise CustomException("Failed to load data", sys) from e