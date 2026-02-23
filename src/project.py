import os
from pathlib import Path
from typing import Optional
import json
from pathlib import Path


# def get_project_dir() -> str:
#     return os.path.abspath(os.path.dirname(__file__))
def find_project_dir(start_path: Optional[str] = None) -> Path:
    """
    Find the project directory containing a pyproject.toml file.

    Searches upward from the start_path (or current file's location) until it finds
    a directory containing pyproject.toml. If not found, returns the directory
    containing the current file.

    Args:
        start_path: Optional starting path to search from. If None, uses the
                   directory of the file where this function is called.

    Returns:
        Path object pointing to the project directory

    Raises:
        FileNotFoundError: If no pyproject.toml is found and the starting path doesn't exist
    """
    # Determine starting point
    if start_path is None:
        # Get the directory of the file that called this function
        import inspect
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        start_path = os.path.dirname(os.path.abspath(caller_file))

    current_path = Path(start_path).resolve()

    if not current_path.exists():
        raise FileNotFoundError(f"Starting path does not exist: {current_path}")

    # Search upward for pyproject.toml
    for parent in [current_path] + list(current_path.parents):
        if (parent / "pyproject.toml").exists():
            return parent

    # If not found, return the starting directory
    return current_path


# Convenience function for common use case
def get_project_dir() -> Path:
    """
    Get the project directory containing pyproject.toml.

    Returns the directory containing pyproject.toml by searching upward from
    the location of this file. If no pyproject.toml is found, returns the
    directory containing this file.
    """
    return find_project_dir()


def write_json_file(path: Path | str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def read_json_file(path: Path | str):
    with open(path) as json_file:
        data = json.load(json_file)
    return data
