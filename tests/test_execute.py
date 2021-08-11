import lox

import pytest

@pytest.mark.parametrize(
    "input_str,expected",
    [
        (
            'print "foo";',
            "foo",
        ),
        (
            '''print "one"; print true; print 2 + 1;''',
            "one\ntrue\n3",
        ),
        (
            'var a = 3; print a + 2;',
            "5",
        ),
        (
            'var a = 3; print a + 2; a = a + 2; print a;',
            "5\n5",
        ),
    ]
)
def test_scripts(capsys, input_str, expected):
    runtime = lox.Lox()
    runtime.run(input_str)
    captured = capsys.readouterr()
    assert captured.err == ""
    assert captured.out == expected + "\n"
