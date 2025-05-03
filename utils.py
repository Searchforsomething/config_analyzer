import json
import os
import sys
from typing import Callable, Optional


def get_unique_filename(name: str, extension: str, folder: str) -> str:
    if not os.path.exists(os.path.join(folder, f'{name}.{extension}')):
        return os.path.join(folder, f'{name}.{extension}')

    index = 1
    while os.path.exists(os.path.join(folder, f'{name}({index}).{extension}')):
        index += 1

    file_path = os.path.join(folder, f'{name}({index}).{extension}')
    return file_path


def load_and_validate_json(path: str, custom_validator: Optional[Callable[[dict], None]] = None) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f'Error reading JSON from {path}: {e}', file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f'File not found: {path}', file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f'Error: JSON in {path} must be dict, not {type(data).__name__}', file=sys.stderr)
        sys.exit(1)

    if custom_validator:
        custom_validator(data)

    return data


def validate_config_json(data: dict) -> None:
    for k, v in data.items():
        if not isinstance(k, str):
            print(f'Error: keys in file must be str. Found: {k}: {v}', file=sys.stderr)
            sys.exit(1)

    return
