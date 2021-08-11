import lox

import pytest

@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            "3",
            3
        ),
        (
            "1 + 2",
            3
        ),
        (
            "1 - 2",
            -1
        ),
        (
            "12 * 6",
            72
        ),
        (
            "1.2 * 6",
            # Need to calculate this for matching rounding errors
            1.2 * 6
        ),
        (
            "6 / 4",
            1.5
        ),
        (
            "6.2 > 43.0",
            False
        ),
        (
            "60.2 <= 43.0",
            False
        ),
        (
            '("foo" + "bar") == "foobar"',
            True
        ),
        (
            "(60.2 <= 43.0) == false",
            True
        ),
        (
            "60.2 <= 43.0 == false",
            True
        ),
        (
            "!false",
            True
        ),
        (
            "!true",
            False
        ),
        (
            "!true == false",
            True
        ),
        (
            "4 != 4",
            False
        ),
        (
            '"foo" + "bar"',
            "foobar",
        ),
    ]
)
def test_scripts(input_str, expected):
    assert lox.Interpreter.evaluate_str(input_str) == expected
