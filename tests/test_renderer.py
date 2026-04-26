import os
import pytest

import src.renderer
from src.dates import normalize_date
from src.models import Person
from src.renderer import HEADERS, TITLE, TableWidthError, render_people_table


@pytest.fixture
def set_terminal_width(monkeypatch):
    def set_width(width: int) -> None:
        """Устанавливает фиктивную ширину терминала для рендера таблицы"""
        monkeypatch.setattr(
            src.renderer.shutil,
            "get_terminal_size",
            lambda fallback=(120, 20): os.terminal_size((width, 20))
        )

    return set_width


def test_render_people_table_renders_title_headers_and_rows(set_terminal_width):
    """Проверяет базовую отрисовку заголовка, шапки и данных"""
    set_terminal_width(90)
    people = [
        Person(
            full_name="Иванов Иван",
            age="30",
            address="улица Ленина, 1",
            birth_date="2022-12-23 05:56:06",
        )
    ]

    table = render_people_table(people)

    assert TITLE in table
    assert HEADERS[0] in table
    assert HEADERS[1] in table
    assert HEADERS[2] in table
    assert HEADERS[3] in table
    assert "Иванов Иван" in table
    assert "30" in table
    assert "улица Ленина, 1" in table
    assert "2022-12-23 05:56:06" in table


def test_render_people_table_shortens_values_to_requested_width(set_terminal_width):
    """Проверяет сокращение длинных значений по доступной ширине"""
    set_terminal_width(65)
    people = [
        Person(
            full_name="Очень Длинное Имя Которое Не Помещается",
            age="30",
            address="Очень длинный адрес который точно не помещается",
            birth_date="2022-12-23 05:56:06"
        )
    ]

    table = render_people_table(people)

    assert "..." in table
    assert all(len(line) <= 65 for line in table.splitlines())


def test_render_people_table_raises_error_when_width_is_too_small(set_terminal_width):
    """Проверяет исключение при слишком узком терминале"""
    set_terminal_width(59)
    people = [
        Person(
            full_name="Иванов Иван",
            age="30",
            address="улица Ленина, 1",
            birth_date=normalize_date("2022-12-23 05:56:06"),
        )
    ]

    with pytest.raises(TableWidthError):
        render_people_table(people)
