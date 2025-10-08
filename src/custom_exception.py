"""
custom_exception.py
-------------------
Defines a custom exception class for unified and descriptive error handling
throughout the MLOps project.

This module standardises how exceptions are raised and reported by including
information such as the file name and line number where the error occurred.

Usage
-----
Example (within any module):

    from src.custom_exception import CustomException
    import sys

    try:
        result = 10 / 0
    except Exception as e:
        raise CustomException(str(e), sys)

Notes
-----
- The exception message includes both the file name and line number.
- Use this for consistent and informative error handling across all modules.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------
import sys
import traceback


# -------------------------------------------------------------------
# Custom Exception Class
# -------------------------------------------------------------------
class CustomException(Exception):
    """
    A custom exception class that enhances error messages with
    detailed context (file name and line number).

    Parameters
    ----------
    error_message : str
        The original error message to be displayed.
    error_detail : sys
        The system module providing traceback details.

    Attributes
    ----------
    error_message : str
        The formatted error message including file name and line number.
    """

    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    # -------------------------------------------------------------------
    # Static Method: Error Message Formatter
    # -------------------------------------------------------------------
    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: sys) -> str:
        """
        Constructs a detailed error message containing the file name,
        line number, and original error text.

        Parameters
        ----------
        error_message : str
            The message describing the error.
        error_detail : sys
            The system module, used to extract traceback details.

        Returns
        -------
        str
            A formatted message including file name and line number.
        """
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error in {file_name}, line {line_number}: {error_message}"

    # -------------------------------------------------------------------
    # String Representation
    # -------------------------------------------------------------------
    def __str__(self) -> str:
        """
        Returns the formatted error message when the exception is printed.

        Returns
        -------
        str
            The descriptive error message.
        """
        return self.error_message