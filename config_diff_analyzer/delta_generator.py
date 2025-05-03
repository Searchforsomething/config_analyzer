import json

from utils import get_unique_filename, load_and_validate_json, validate_config_json


def generate_delta(config_path: str, patched_path: str, output_dir: str) -> str:
    config = load_and_validate_json(config_path, validate_config_json)
    patched = load_and_validate_json(patched_path, validate_config_json)

    additions = [
        {'key': k, 'value': v}
        for k, v in patched.items() if k not in config
    ]
    deletions = [k for k in config if k not in patched]
    updates = [
        {'key': k, 'from': config[k], 'to': patched[k]}
        for k in config if k in patched and config[k] != patched[k]
    ]

    delta = {
        'additions': additions,
        'deletions': deletions,
        'updates': updates
    }

    delta_path = get_unique_filename('delta', 'json', output_dir)

    with open(delta_path, 'a+') as file:
        json.dump(delta, file, indent=4)

    print(f'Result saved to {delta_path}')

    return delta_path
