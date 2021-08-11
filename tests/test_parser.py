import lox

import pytest

@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("3", lox.LiteralExpr(3)),
        ('"foo"', lox.LiteralExpr("foo")),
        ('nil', lox.LiteralExpr(None)),
        ('false', lox.LiteralExpr(False)),
        ('(3)', lox.GroupingExpr(lox.LiteralExpr(3))),
        ('3 + "foo"',
            lox.BinaryExpr(
                lox.LiteralExpr(3),
                lox.Token(token_type=lox.Plus()),
                lox.LiteralExpr("foo"),
            )
        ),
        (
            '3 + 4 * 6 + 8',
            lox.BinaryExpr(
                lox.BinaryExpr(
                    lox.LiteralExpr(3),
                    lox.Token(lox.Plus()),
                    lox.BinaryExpr(
                        lox.LiteralExpr(4),
                        lox.Token(lox.Star()),
                        lox.LiteralExpr(6),
                    )
                ),
                lox.Token(lox.Plus()),
                lox.LiteralExpr(8),
            )
        ),
        ('(3 + "foo")',
            lox.GroupingExpr(
                lox.BinaryExpr(
                    lox.LiteralExpr(3),
                    lox.Token(token_type=lox.Plus()),
                    lox.LiteralExpr("foo"),
                )
            )
        ),
        ('-true',
            lox.UnaryExpr(
                lox.Token(token_type=lox.Minus()),
                lox.LiteralExpr(True),
            )
        ),
        # TODO: I guess idents aren't here yet
        #('some_ident', lox.LiteralExpr(False)),
    ]
)
def test_parse_expression(input_str, expected):
    scanner = lox.Scanner(input_str)
    parser = lox.Parser(scanner.scan_tokens())
    assert parser.expression() == expected
