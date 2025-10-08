"""
setup.py
--------
Project configuration file for packaging and installation of the
**MLOps Project 1** Python package.

This script uses `setuptools` to define the package metadata,
dependencies, and build configuration. It enables consistent installation
of the project both locally and within CI/CD pipelines.

Usage
-----
Standard installation (from project root):
    pip install .

Editable (development) installation:
    pip install -e .

To build and distribute the package:
    python setup.py sdist bdist_wheel

Notes
-----
- Ensure `requirements.txt` contains all runtime dependencies.
- The `find_packages()` call automatically discovers subpackages under `src/`
  or the current directory (depending on project layout).
"""

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
from setuptools import setup, find_packages

# -------------------------------------------------------------------
# Dependency Loading
# -------------------------------------------------------------------
# Read the list of required packages from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# -------------------------------------------------------------------
# Package Configuration
# -------------------------------------------------------------------
setup(
    name="MLOps-Hotel-Reservation-Prediction",          # 📦 Package name
    version="0.1",                                      # 🔢 Initial version
    author="Ch3rry Pi3",                                # 👤 Author name
    packages=find_packages(),                           # 📂 Automatically include all subpackages
    install_requires=requirements,                      # 📜 Runtime dependencies
)
