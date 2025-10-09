"""
model_params.py
----------------
Hyperparameter configuration module for the MLOps Hotel Reservation Prediction project.

This file defines the **LightGBM search space** and **RandomizedSearchCV parameters**
used during the model training stage. The parameter ranges are intentionally broad
to allow for flexible experimentation while maintaining computational efficiency.

Usage
-----
Example:
    from config.model_params import LIGHTGBM_PARAMS, RANDOM_SEARCH_PARAMS

Notes
-----
- The search spaces leverage SciPy distributions for continuous sampling.
- These parameters are used in conjunction with `RandomizedSearchCV`.
- Adjust `n_iter` and `cv` for more exhaustive or faster searches.
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
from scipy.stats import randint, uniform

# -------------------------------------------------------------------
# 🌳 LIGHTGBM HYPERPARAMETER SPACE
# -------------------------------------------------------------------
LIGHTGBM_PARAMS = {
    'n_estimators': randint(100, 500),          # Number of boosting rounds
    'max_depth': randint(5, 50),                # Depth of each tree
    'learning_rate': uniform(0.01, 0.2),        # Step size shrinkage
    'num_leaves': randint(20, 100),             # Maximum number of leaves per tree
    'boosting_type': ['gbdt', 'dart']           # Gradient boosting variants
}

# -------------------------------------------------------------------
# 🎯 RANDOMISED SEARCH CONFIGURATION
# -------------------------------------------------------------------
RANDOM_SEARCH_PARAMS = {
    'n_iter': 5,                # Number of random parameter combinations to try
    'cv': 2,                    # Cross-validation folds
    'n_jobs': -1,               # Use all available CPU cores
    'verbose': 2,               # Verbosity level
    'random_state': 5901,       # For reproducibility
    'scoring': 'accuracy'       # Optimisation metric
}