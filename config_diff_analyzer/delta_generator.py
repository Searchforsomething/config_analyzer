import json
import sys

from utils import get_unique_filename


def load_and_validate_json(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f'Ошибка чтения JSON из {path}: {e}', file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f'Файл не найден: {path}', file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, dict):
        print(f'Ошибка: JSON в файле {path} должен быть объектом (dict), а не {type(data).__name__}', file=sys.stderr)
        sys.exit(1)

    for k, v in data.items():
        if not isinstance(k, str) or not isinstance(v, str):
            print(f'Ошибка: ключи и значения в {path} должны быть строками. Найдено: {k}: {v}', file=sys.stderr)
            sys.exit(1)

    return data


def generate_delta(config_path: str, patched_path: str, output_dir: str) -> str:
    config = load_and_validate_json(config_path)
    patched = load_and_validate_json(patched_path)

    additions = [
        {"key": k, "value": v}
        for k, v in patched.items() if k not in config
    ]
    deletions = [k for k in config if k not in patched]
    updates = [
        {"key": k, "from": config[k], "to": patched[k]}
        for k in config if k in patched and config[k] != patched[k]
    ]

    delta = {
        "additions": additions,
        "deletions": deletions,
        "updates": updates
    }

    delta_path = get_unique_filename('delta', 'json', output_dir)

    with open(delta_path, 'a+') as file:
        json.dump(delta, file, indent=4)

    print(f'Результат сохранен в {delta_path}')

    return delta_path
