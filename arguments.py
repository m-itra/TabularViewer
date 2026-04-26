import argparse

DEFAULT_LIMIT = 100


def parse_args(argv):
    """Разбирает аргументы командной строки"""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Читает текстовый файл с записями о людях и выводит отформатированную таблицу в консоль.",
        epilog=(
            "Ожидаемые колонки: ФИО, возраст, адрес, дата. "
            "Источник входных данных может быть локальным путём к файлу или ссылкой."
        ),
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog,
            max_help_position=30,
        ),
    )
    parser.add_argument(
        "-i",
        "--input",
        metavar="PATH",
        required=True,
        help="абсолютный или относительный путь к .txt-файлу либо ссылка",
    )
    parser.add_argument(
        "-s",
        "--start-line",
        metavar="N",
        type=_positive_int,
        default=1,
        help="номер записи, с которой начинать вывод, начиная с 1",
    )
    parser.add_argument(
        "-l",
        "--limit",
        metavar="COUNT",
        type=_parse_limit,
        default=DEFAULT_LIMIT,
        help="максимальное количество выводимых записей или 'all'",
    )
    return parser.parse_args(argv)


def _positive_int(value):
    """Проверяет, что значение это целое положительное число"""
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"ожидалось целое число, получено {value!r}"
        ) from error

    if parsed < 1:
        raise argparse.ArgumentTypeError("значение должно быть больше нуля")

    return parsed


def _parse_limit(value):
    """Проверяет значение ограничения выборки"""
    if value.lower() == "all":
        return None

    return _positive_int(value)
