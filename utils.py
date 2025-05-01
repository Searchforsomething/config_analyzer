import os


def get_unique_filename(name: str, extension: str, folder: str) -> str:
    if not os.path.exists(os.path.join(folder, f'{name}.{extension}')):
        return os.path.join(folder, f'{name}.{extension}')

    index = 1
    while os.path.exists(os.path.join(folder, f'{name}({index}).{extension}')):
        index += 1

    file_path = os.path.join(folder, f'{name}({index}).{extension}')
    return file_path
