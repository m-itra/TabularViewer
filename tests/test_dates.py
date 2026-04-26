import pytest

from src.dates import DateParseError, normalize_date


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2022-12-23 05:56:06", "2022-12-23 05:56:06"),
        ("2022-01-21T09:09:17", "2022-01-21 09:09:17"),
        ("19800713T205307", "1980-07-13 20:53:07"),
        ("2026-15-03 00:00:00", "2026-03-15 00:00:00"),
    ],
)
def test_normalize_date_supports_expected_inputs(value: str, expected: str):
    """Проверяет поддерживаемые форматы входных дат"""
    assert normalize_date(value) == expected


# @pytest.mark.parametrize(
#     "value",
#     [
#         "2010-30-02 05:56:30",
#         "2022-02-31 05:56:06",
#         "2022-12-23 25:00:00",
#         "2022-00-10 00:00:00",
#     ],
# )
# def test_normalize_date_rejects_impossible_date_values(value: str):
#     with pytest.raises(DateParseError):
#         normalize_date(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2010-30-02 05:56:30", "2010-02-30 05:56:30"),
        ("2022-02-31 05:56:06", "2022-02-31 05:56:06"),
        ("2022-12-23 25:00:00", "2022-12-23 25:00:00"),
        ("2022-00-10 00:00:00", "2022-00-10 00:00:00"),
    ],
)
def test_normalize_date_keeps_format_for_impossible_date_values(
        value: str,
        expected: str,
        capsys
):
    """Проверяет вывод предупреждения для невозможной даты"""
    assert normalize_date(value, line_number=7) == expected

    captured = capsys.readouterr()
    assert captured.err == f"В строке 7 невозможная дата: {value!r}\n"


@pytest.mark.parametrize(
    "value",
    [
        "bad-date",
        "2022/12/23 05:56:06",
        "2022-12-23",
    ],
)
def test_normalize_date_rejects_unsupported_formats(value: str):
    """Проверяет, что неподдерживаемые форматы даты вызывают ошибку"""
    with pytest.raises(DateParseError):
        normalize_date(value)
