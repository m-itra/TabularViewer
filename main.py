import sys

from arguments import parse_args
from src.app import render_table
from src.dates import DateParseError
from src.input.reader import InputError
from src.parser import ParseError
from src.renderer import TableWidthError


def main():
    args = parse_args(sys.argv[1:])

    try:
        table = render_table(
            args.input,
            start_line=args.start_line,
            limit=args.limit,
        )
        print(table)
    except InputError as error:
        print(f"Ошибка ввода: {error}", file=sys.stderr)
        return 1
    except ParseError as error:
        print(f"Ошибка разбора: {error}", file=sys.stderr)
        return 1
    except DateParseError as error:
        print(f"Ошибка разбора даты: {error}", file=sys.stderr)
        return 1
    except TableWidthError as error:
        print(f"Ошибка отрисовки таблицы: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Ошибка ввода-вывода: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
