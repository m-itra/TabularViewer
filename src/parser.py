import re
from collections.abc import Iterable, Iterator

from src.models import Person
from src.dates import DateParseError, normalize_date, split_date_tail

AGE_PATTERN = re.compile(r"^\d{1,3}$")
AGE_WITH_ADDRESS_PATTERN = re.compile(r"^\s*(?P<age>\d{1,3})\s+(?P<address>.+?)\s*$")


class ParseError(ValueError):
    pass


def parse_people(lines: Iterable[str], start_line_number: int = 1) -> Iterator[Person]:
    """Преобразует последовательность строк в объекты Person"""
    for line_number, line in enumerate(lines, start=start_line_number):
        try:
            yield parse_line(line, line_number=line_number)
        except DateParseError as exc:
            raise DateParseError(f"строка {line_number}: {exc}") from exc
        except ParseError as exc:
            raise ParseError(f"строка {line_number}: {exc}") from exc


def parse_line(line: str, line_number: int | None = None) -> Person:
    """Разбирает одну строку записи о человеке"""
    before_date, raw_date = split_date_tail(line)
    fields = [field.strip() for field in before_date.split("\t")]

    full_name = fields[0]
    age, address = _parse_age_and_address(fields[1:])

    if not full_name: raise ParseError("поле ФИО пустое")
    if not age: raise ParseError("поле возраста пустое")
    if not address: raise ParseError("поле адреса пустое")

    return Person(
        full_name=full_name,
        age=age,
        address=address,
        birth_date=normalize_date(raw_date, line_number),
    )


def _parse_age_and_address(fields: list[str]) -> tuple[str, str]:
    """Извлекает возраст и адрес из полей"""
    non_empty_fields = [field for field in fields if field]

    if AGE_PATTERN.match(non_empty_fields[0]):
        return non_empty_fields[0], _join_fields(non_empty_fields[1:])

    match = AGE_WITH_ADDRESS_PATTERN.match(non_empty_fields[0])
    if match:
        address_parts = [match.group("address"), *non_empty_fields[1:]]
        return match.group("age"), _join_fields(address_parts)

    return "", _join_fields(non_empty_fields)


def _join_fields(fields: list[str]) -> str:
    """Склеивает части поля в одну строку"""
    return " ".join(fields).strip()
