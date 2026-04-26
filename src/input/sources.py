from pathlib import Path
from urllib.request import urlopen
from collections.abc import Iterator
from contextlib import contextmanager


@contextmanager
def open_input_stream(input_value: str) -> Iterator[object]:
    """Открывает локальный файл или URL как бинарный поток"""
    if input_value.startswith(("http://", "https://")):
        with urlopen(input_value) as response:
            yield response
        return

    path = Path(input_value).expanduser()
    with path.open("rb") as file:
        yield file
