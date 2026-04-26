import shutil

from collections.abc import Iterable, Sequence

from src.models import Person

TITLE = "Список людей"
HEADERS = ("ФИО", "Возраст", "Адрес", "Дата рождения")
MIN_WIDTHS = (11, 7, 11, 19)


class TableWidthError(ValueError):
    pass


def render_people_table(people: Iterable[Person]) -> str:
    """Строит текстовую таблицу со списком людей"""
    table_width = shutil.get_terminal_size(fallback=(120, 20)).columns
    rows, content_widths = _collect_rows(people)
    column_widths = _calculate_column_widths(content_widths, table_width)

    return "\n".join(
        [
            TITLE.center(table_width),
            _render_separator(
                column_widths,
                left="╭",
                middle="┬",
                right="╮",
            ),
            _render_row(HEADERS, column_widths),
            _render_separator(
                column_widths,
                left="├",
                middle="┼",
                right="┤",
            ),
            *(_render_row(row, column_widths) for row in rows),
            _render_separator(
                column_widths,
                left="╰",
                middle="┴",
                right="╯",
            )
        ]
    )


def _collect_rows(people: Iterable[Person]) -> tuple[list[tuple[str, ...]], list[int]]:
    """Собирает строки таблицы и определяет максимальные ширины колонок"""
    rows = []
    widths = [len(header) for header in HEADERS]
    for person in people:
        row = (
            person.full_name,
            person.age,
            person.address,
            person.birth_date,
        )
        rows.append(row)

        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    return rows, widths


def _calculate_column_widths(widths: Sequence[int], table_width: int) -> list[int]:
    """Подбирает итоговые ширины колонок под текущую ширину терминала"""
    min_table_width = _actual_table_width(MIN_WIDTHS)

    if table_width < min_table_width:
        raise TableWidthError(
            "ширина консоли слишком маленькая для читаемой таблицы: "
            f"минимум {min_table_width}, сейчас {table_width}"
        )

    available_width = table_width - (len(widths) * 3 + 1)
    column_widths = _shrink_widths(
        list(widths),
        list(MIN_WIDTHS),
        available_width,
    )

    if sum(column_widths) < available_width:
        column_widths[2] += available_width - sum(column_widths)

    return column_widths


def _shrink_widths(widths: list[int], minimums: list[int], available_width: int) -> list[int]:
    """Уменьшает ширины колонок, пока таблица не поместится в доступное место"""

    while sum(widths) > available_width:
        index = _find_most_shrinkable_column(widths, minimums)

        if index is None:
            break

        widths[index] -= 1

    return widths


def _find_most_shrinkable_column(widths: list[int], minimums: list[int]) -> int | None:
    """Находит колонку с наибольшим запасом по ширине"""
    best_index = None
    best_extra_width = 0

    for index, (width, minimum) in enumerate(zip(widths, minimums)):
        extra_width = width - minimum

        if extra_width > best_extra_width:
            best_index = index
            best_extra_width = extra_width

    return best_index


def _actual_table_width(column_widths: Sequence[int]) -> int:
    """Возвращает полную ширину таблицы с учётом рамок и отступов"""
    return sum(column_widths) + len(column_widths) * 3 + 1


def _render_separator(
        column_widths: Sequence[int],
        left: str = "├",
        middle: str = "┼",
        right: str = "┤",
        horizontal: str = "─",
) -> str:
    """Формирует строку-разделитель таблицы"""
    return (
            left
            + middle.join(horizontal * (width + 2) for width in column_widths)
            + right
    )


def _render_row(values: Sequence[str], column_widths: Sequence[int]) -> str:
    """Формирует одну строку таблицы с учётом ширин колонок"""
    cells = []

    for value, width in zip(values, column_widths):
        fitted_text = _fit_text(value, width)
        cell = f" {fitted_text:<{width}} "
        cells.append(cell)

    return "|" + "|".join(cells) + "|"


def _fit_text(value: str, width: int) -> str:
    """Обрезает текст по ширине и добавляет многоточие при необходимости"""
    if len(value) <= width:
        return value

    return value[:width - 3] + "..."
