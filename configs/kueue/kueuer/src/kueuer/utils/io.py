"""Input/Output utilities for reading and writing files."""

import csv
import os
from datetime import datetime
from typing import Any, Dict, List, Set

import yaml

from kueuer.utils.logging import logger


def read_yaml(filepath: str) -> Dict[Any, Any]:
    """Reads a YAML file and returns its content as a dictionary.

    Args:
        filepath (str): Path to the YAML file.

    Returns:
        Dict[Any, Any]: Content of the YAML file as a dictionary.
    """
    with open(filepath, encoding="utf-8") as f:
        data = f.read()
        return yaml.safe_load(data)


def save_results_to_csv(results: List[Dict[str, Any]], filename: str) -> None:
    """
    Save benchmark results to a CSV file.

    Args:
        results: List of experiment result dictionaries
        filename: Path to save CSV file
    """
    # Define fieldnames based on all possible keys in results
    fieldnames: Set[str] = set()
    for result in results:
        fieldnames.update(result.keys())
    fieldnames = sorted(fieldnames)  # type: ignore

    # Check if file exists to determine if header is needed
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for result in results:
            # Handle datetime objects by converting them to strings
            row_data = {}
            for key, value in result.items():
                if isinstance(value, datetime):
                    row_data[key] = value.isoformat()
                else:
                    row_data[key] = value
            writer.writerow(row_data)  # type: ignore

    logger.info("Results saved to %s", filename)
