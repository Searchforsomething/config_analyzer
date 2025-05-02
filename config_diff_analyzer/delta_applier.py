import json

from utils import get_unique_filename


def apply_delta(config_path: str, delta_path: str, output_dir: str) -> None:
    with open(config_path) as f:
        config = json.load(f)
    with open(delta_path) as f:
        delta = json.load(f)

    for key in delta.get("deletions", []):
        config.pop(key, None)
    for update in delta.get("updates", []):
        config[update["key"]] = update["to"]
    for addition in delta.get("additions", []):
        config[addition["key"]] = addition["value"]

    result_path = get_unique_filename('res_patched_config', 'json', output_dir)

    with open(result_path, 'a+') as file:
        json.dump(config, file, indent=4)

    print(f'Результат сохранен в {result_path}')

    return
