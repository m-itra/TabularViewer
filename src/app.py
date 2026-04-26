from itertools import islice

from src.input.reader import iter_input_lines
from src.parser import parse_people
from src.renderer import render_people_table


def render_table(input_value: str, start_line: int, limit: int | None) -> str:
    """Читает записи из источника и возвращает отформатированную таблицу"""
    record_lines = (line for line in iter_input_lines(input_value) if line.strip())

    stop = None if limit is None else start_line - 1 + limit
    selected_lines = islice(record_lines, start_line - 1, stop)

    return render_people_table(
        parse_people(selected_lines, start_line_number=start_line)
    )
