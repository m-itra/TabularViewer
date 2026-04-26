import io
from pathlib import Path
from unittest.mock import patch

from src.app import render_table


class BytesResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.close()


def _write_temp_input(lines: list[str]) -> Path:
    """Создаёт временный входной файл для тестов"""
    path = Path("tests") / "people.txt"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def test_render_table_can_render_window_from_input_file():
    """Проверяет отрисовку выбранного диапазона строк из файла"""
    path = _write_temp_input(
        [
            "Alice Smith\t30\tStreet 1\t2022-12-23 05:56:06",
            "Bob Smith\t31\tStreet 2\t2022-12-24 05:56:06",
            "Cara Smith\t32\tStreet 3\t2022-12-25 05:56:06",
            "Dan Smith\t33\tStreet 4\t2022-12-26 05:56:06",
        ]
    )

    try:
        table = render_table(str(path), start_line=2, limit=2)
    finally:
        if path.exists():
            path.unlink()

    assert "Alice Smith" not in table
    assert "Bob Smith" in table
    assert "Cara Smith" in table
    assert "Dan Smith" not in table


def test_render_table_accepts_url_input_stream():
    """Проверяет чтение входных данных по URL"""
    data = b"Alice Smith\t30\tStreet 1\t2022-12-23 05:56:06\n"

    with patch("src.input.sources.urlopen", return_value=BytesResponse(data)) as mocked_urlopen:
        table = render_table(
            "https://example.test/data.txt",
            start_line=1,
            limit=1,
        )

    mocked_urlopen.assert_called_once_with("https://example.test/data.txt")
    assert "Alice Smith" in table


def test_render_table_skips_parsing_records_before_selected_window():
    """Проверяет, что строки до выбранного окна не разбираются"""
    path = _write_temp_input(
        [
            "Bad Input\tmissing date",
            "Bob Smith\t31\tStreet 2\t2022-12-24 05:56:06",
        ]
    )

    try:
        table = render_table(str(path), start_line=2, limit=1)
    finally:
        if path.exists():
            path.unlink()

    assert "Bob Smith" in table
