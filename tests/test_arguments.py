import pytest

from arguments import DEFAULT_LIMIT, parse_args


def test_parse_args_uses_default_limit():
    """Проверяет использование лимита по умолчанию."""
    args = parse_args(["-i", "data.txt"])

    assert args.limit == DEFAULT_LIMIT


def test_parse_args_parses_input_window_arguments():
    """Проверяет разбор аргументов"""
    args = parse_args(
        ["-i", "data.txt", "--start-line", "10", "--limit", "25"]
    )

    assert args.input == "data.txt"
    assert args.start_line == 10
    assert args.limit == 25


def test_parse_args_parses_short_input_window_arguments():
    """Проверяет разбор коротких аргументов"""
    args = parse_args(["-i", "data.txt", "-s", "10", "-l", "25"])

    assert args.input == "data.txt"
    assert args.start_line == 10
    assert args.limit == 25


def test_parse_args_parses_absent_limit_value():
    """Проверяет значение лимита без ограничения"""
    args = parse_args(["-i", "data.txt", "--limit", "all"])

    assert args.limit is None


def test_parse_args_rejects_zero_start_line():
    """Проверяет, что нулевой номер стартовой строки не принимается"""
    with pytest.raises(SystemExit):
        parse_args(["-i", "data.txt", "--start-line", "0"])


def test_parse_args_rejects_negative_limit():
    """Проверяет, что отрицательный лимит не принимается"""
    with pytest.raises(SystemExit):
        parse_args(["-i", "data.txt", "--limit", "-1"])
