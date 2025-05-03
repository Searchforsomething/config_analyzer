import json
import sys

from utils import get_unique_filename, load_and_validate_json, validate_config_json


def validate_delta_json(data: dict) -> None:
    allowed_keys = ['additions', 'deletions', 'updates']
    for key in data.keys():
        if key not in allowed_keys:
            print(f'Unknown key in delta.json: "{key}"', file=sys.stderr)
            sys.exit(1)

    return


def apply_delta(config_path: str, delta_path: str, output_dir: str) -> None:
    config = load_and_validate_json(config_path, validate_config_json)
    delta = load_and_validate_json(delta_path, validate_delta_json)

    for key in delta.get('deletions', []):
        config.pop(key, None)
    for update in delta.get('updates', []):
        config[update['key']] = update['to']
    for addition in delta.get('additions', []):
        config[addition['key']] = addition['value']

    result_path = get_unique_filename('res_patched_config', 'json', output_dir)

    with open(result_path, 'a+') as file:
        json.dump(config, file, indent=4)

    print(f'Result saved to {result_path}')
    return
