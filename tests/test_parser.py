import pytest

from src.parser import ParseError, parse_line, parse_people

FULL_NAME = "Иван Иванов"
AGE = "30"
ADDRESS = "Улица Ленина, 1"
BIRTH_DATE = "2022-12-23 05:56:06"
INVALID_BIRTH_DATE = "2022-02-31 05:56:06"


def test_parse_line_parses_normal_tab_separated_line():
    """Проверяет разбор корректной строки"""
    person = parse_line(f"{FULL_NAME}\t{AGE}\t{ADDRESS}\t{BIRTH_DATE}")

    assert person.full_name == FULL_NAME
    assert person.age == AGE
    assert person.address == ADDRESS
    assert person.birth_date == BIRTH_DATE


def test_parse_line_ignores_empty_field_before_age():
    """Проверяет игнорирование пустого поля"""
    person = parse_line(f"{FULL_NAME}\t\t{AGE}			{ADDRESS}\t{BIRTH_DATE}")

    assert person.full_name == FULL_NAME
    assert person.age == AGE
    assert person.address == ADDRESS
    assert person.birth_date == BIRTH_DATE


def test_parse_line_rejects_empty_full_name_without_shifting_columns():
    """Проверяет ошибку при пустом имени"""
    with pytest.raises(ParseError, match="поле ФИО пустое"):
        parse_line(f"\t{AGE}\t{ADDRESS}\t{BIRTH_DATE}")


# def test_parse_people_rejects_semantically_invalid_date():
#     with pytest.raises(DateParseError):
#         list(parse_people([f"{FULL_NAME}\t{AGE}\t{ADDRESS}\t{INVALID_BIRTH_DATE}"]))


def test_parse_people_keeps_semantically_invalid_date_and_writes_warning(capsys):
    """Проверяет сохранение невозможной даты и вывод предупреждения."""
    people = list(parse_people([f"{FULL_NAME}\t{AGE}\t{ADDRESS}\t{INVALID_BIRTH_DATE}"]))

    assert len(people) == 1
    assert people[0].birth_date == INVALID_BIRTH_DATE

    captured = capsys.readouterr()
    assert captured.err == f"В строке 1 невозможная дата: {INVALID_BIRTH_DATE!r}\n"
