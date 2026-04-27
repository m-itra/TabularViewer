import sys

from arguments import parse_args
from src.app import render_table
from src.dates import DateParseError
from src.input.reader import InputError
from src.parser import ParseError
from src.renderer import TableWidthError

ERROR_LABELS = {
    InputError: "Ошибка ввода",
    ParseError: "Ошибка разбора",
    DateParseError: "Ошибка разбора даты",
    TableWidthError: "Ошибка отрисовки таблицы",
}

HANDLED_ERRORS = tuple(ERROR_LABELS)


def format_error(error: Exception) -> str:
    for error_type, label in ERROR_LABELS.items():
        if isinstance(error, error_type):
            return f"{label}: {error}"

    return f"Ошибка: {error}"


def main():
    args = parse_args(sys.argv[1:])

    try:
        table = render_table(args.input, start_line=args.start_line, limit=args.limit)
    except HANDLED_ERRORS as error:
        print(format_error(error), file=sys.stderr)
        return 1

    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
