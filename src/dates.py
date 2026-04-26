import re
import sys

from datetime import datetime

DATE_PATTERN = re.compile(
    r"""^\s*
    (?P<year>\d{4})
    (?:
        -(?P<month>\d{2})-(?P<day>\d{2})
        |
        (?P<compact_month>\d{2})(?P<compact_day>\d{2})
    )
    [ T]
    (?:
        (?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})
        |
        (?P<compact_hour>\d{2})(?P<compact_minute>\d{2})(?P<compact_second>\d{2})
    )
    \s*$
    """,
    re.VERBOSE,
)

DATE_TAIL_PATTERN = re.compile(
    r"""
    (?P<date>
        \d{4}
        (?:
            -\d{2}-\d{2}
            |
            \d{4}
        )
        [ T]
        (?:
            \d{2}:\d{2}:\d{2}
            |
            \d{6}
        )
    )
    \s*$
    """,
    re.VERBOSE,
)


class DateParseError(ValueError):
    pass


def split_date_tail(line: str) -> tuple[str, str]:
    """Отделяет дату в конце строки от остальных полей."""
    match = DATE_TAIL_PATTERN.search(line)
    if match is None:
        raise DateParseError("дата не найдена в конце строки")

    raw_date = match.group("date")
    before_date = line[:match.start()].rstrip()
    return before_date, raw_date


def normalize_date(value: str, line_number: int | None = None) -> str:
    """Приводит дату к единому формату"""
    raw = value.strip()
    match = DATE_PATTERN.match(raw)
    if match is None:
        raise DateParseError(f"неподдерживаемый формат даты: {value!r}")

    year = int(match.group("year"))
    month = int(match.group("month") or match.group("compact_month"))
    day = int(match.group("day") or match.group("compact_day"))

    if month > 12:
        month, day = day, month

    hour = int(match.group("hour") or match.group("compact_hour") or 0)
    minute = int(match.group("minute") or match.group("compact_minute") or 0)
    second = int(match.group("second") or match.group("compact_second") or 0)

    # _validate_date_parts(value, year, month, day, hour, minute, second)

    if not _validate_date_parts(value, year, month, day, hour, minute, second):
        print(f"В строке {line_number} невозможная дата: {value!r}", file=sys.stderr)

    return (
        f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    )


def _validate_date_parts(
        raw_value: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
) -> bool:
    """Проверяет, что дата возможна"""
    try:
        datetime(year, month, day, hour, minute, second)
    except ValueError:
        # try:
        #     datetime(year, month, day, hour, minute, second)
        # except ValueError as error:
        #     raise DateParseError(f"impossible date value: {raw_value!r}") from error
        return False

    return True
