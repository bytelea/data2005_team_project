import json
from pathlib import Path
import pandas as pd


# This error is raised when a file cannot be loaded
class LoadError(Exception):
    pass


def load_data(filepath):
    path = Path(filepath)

    # Check if the file exists
    if not path.exists():
        raise LoadError(f"File not found: {path}")

    # Check if the file type is supported
    file_type = path.suffix.lower()
    if file_type not in [".csv", ".json"]:
        raise LoadError(f"File type '{file_type}' is not supported. Use .csv or .json")

    # Try to load the file
    try:
        if file_type == ".csv":
            df = load_csv(path)
        else:
            df = load_json(path)
    except LoadError:
        raise
    except Exception as error:
        raise LoadError(f"Could not read '{path.name}': {error}")

    # Check the file has data in it
    if df.empty:
        raise LoadError(f"The file has no data: {path}")

    return df


def load_csv(path):
    # Try different encodings in case the file uses special characters
    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            df = pd.read_csv(path, encoding=encoding, low_memory=False)
            df.columns = df.columns.str.strip()
            return df
        except UnicodeDecodeError:
            # This encoding didn't work, try the next one
            continue
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
        except pd.errors.ParserError as error:
            raise LoadError(f"CSV error in '{path.name}': {error}")

    raise LoadError(f"Could not read '{path.name}' — tried all encodings.")


def load_json(path):
    # Open and read the JSON file
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # If it's a list of records, convert directly to a table
    if isinstance(data, list):
        return pd.DataFrame(data)

    # If it's a single object, wrap it in a list first
    if isinstance(data, dict):
        return pd.DataFrame([data])

    raise LoadError(f"Unexpected format in '{path.name}'. Expected a list or dict.")
