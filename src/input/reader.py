from pathlib import Path
from collections.abc import Iterator

from src.input.decoding import iter_decoded_lines
from src.input.sources import open_input_stream


class InputError(ValueError):
    pass


def iter_input_lines(input_value: str) -> Iterator[str]:
    """Открывает источник данных и возвращает декодированные строки"""
    try:
        with open_input_stream(input_value) as binary_stream:
            yield from iter_decoded_lines(binary_stream)
    except FileNotFoundError as error:
        path = Path(input_value).expanduser()
        raise InputError(f"не удалось найти файл {path}") from error
    except OSError as error:
        raise InputError(str(error)) from error
