import lox

import pytest

# For tokens, the lexeme and line are ignored in comparison. This is a stricter
# test that ensures these match exactly, when we mostly don't care otherwise.
def strictly_compare_token_lists(result_tokens, expected_tokens):
    assert len(result_tokens) == len(expected_tokens)
    for result, expected in zip(result_tokens, expected_tokens):
        for attr in ("token_type", "lexeme", "literal", "line"):
            assert getattr(result, attr) == getattr(expected, attr)

def test_sanity():
    text = "{"
    scanner = lox.Scanner(text)
    strictly_compare_token_lists(
        scanner.scan_tokens(),
        [
            lox.Token(
                token_type=lox.LeftBrace(),
                lexeme="{",
                literal=None,
                line=1,
            ),
            lox.Token(
                token_type=lox.EndOfFile(),
                lexeme="",
                literal=None,
                line=1,
            ),
        ]
    )


def test_book_example():
    text = """// this is a comment
(( )){} // grouping stuff
!*+-/=<> <= == // operators
.,;"""
    scanner = lox.Scanner(text)
    assert [token.token_type for token in scanner.scan_tokens()] == [
        # First line
        lox.LeftParen(),
        lox.LeftParen(),
        lox.RightParen(),
        lox.RightParen(),
        lox.LeftBrace(),
        lox.RightBrace(),

        # Second line
        lox.Bang(),
        lox.Star(),
        lox.Plus(),
        lox.Minus(),
        lox.Slash(),
        lox.Equal(),
        lox.Less(),
        lox.Greater(),
        lox.LessEqual(),
        lox.DoubleEqual(),

        # Third line
        lox.Dot(),
        lox.Comma(),
        lox.Semicolon(),

        # EOF that every input gets
        lox.EndOfFile(),
    ]


def test_simple_string():
    text = '"test" + "thing"'
    scanner = lox.Scanner(text)
    assert scanner.scan_tokens() == [
        lox.Token(
            token_type=lox.String(),
            lexeme='"test"',
            literal="test",
            line=1,
        ),
        lox.Token(
            token_type=lox.Plus(),
            lexeme="+",
            literal=None,
            line=1,
        ),
        lox.Token(
            token_type=lox.String(),
            lexeme='"thing"',
            literal="thing",
            line=1,
        ),
        lox.Token(
            token_type=lox.EndOfFile(),
            lexeme="",
            literal=None,
            line=1,
        ),
    ]


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "1234",
            [
                lox.Token(
                    token_type=lox.Number(),
                    lexeme='1234',
                    literal=1234,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.EndOfFile(),
                    lexeme="",
                    literal=None,
                    line=1,
                ),
            ]
        ),
        (
            "3.141592",
            [
                lox.Token(
                    token_type=lox.Number(),
                    lexeme='3.141592',
                    literal=3.141592,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.EndOfFile(),
                    lexeme="",
                    literal=None,
                    line=1,
                ),
            ]
        ),
        (
            "14 + -3.6\n * 4",
            [
                lox.Token(
                    token_type=lox.Number(),
                    lexeme='14',
                    literal=14,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Plus(),
                    lexeme="+",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Minus(),
                    lexeme="-",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Number(),
                    lexeme="3.6",
                    literal=3.6,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Star(),
                    lexeme="*",
                    literal=None,
                    line=2,
                ),
                lox.Token(
                    token_type=lox.Number(),
                    lexeme="4",
                    literal=4,
                    line=2,
                ),
                lox.Token(
                    token_type=lox.EndOfFile(),
                    lexeme="",
                    literal=None,
                    line=2,
                ),
            ]
        ),
    ]
)
def test_number_parsing(text, expected):
    scanner = lox.Scanner(text)
    assert scanner.scan_tokens() == expected

@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "123foo-bar",
            [
                lox.Token(
                    token_type=lox.Number(),
                    lexeme='123',
                    literal=123,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Identifier(),
                    lexeme="foo",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Minus(),
                    lexeme="-",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Identifier(),
                    lexeme="bar",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.EndOfFile(),
                    lexeme="",
                    literal=None,
                    line=1,
                ),
            ]
        ),
    ]
)
def test_number_parsing(text, expected):
    scanner = lox.Scanner(text)
    assert scanner.scan_tokens() == expected

@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "and if or else else2",
            [
                lox.Token(
                    token_type=lox.AndToken(),
                    lexeme='and',
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.IfToken(),
                    lexeme="if",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.OrToken(),
                    lexeme="or",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.ElseToken(),
                    lexeme="else",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.Identifier(),
                    lexeme="else2",
                    literal=None,
                    line=1,
                ),
                lox.Token(
                    token_type=lox.EndOfFile(),
                    lexeme="",
                    literal=None,
                    line=1,
                ),
            ]
        ),
    ]
)
def test_keyword_parsing(text, expected):
    scanner = lox.Scanner(text)
    assert scanner.scan_tokens() == expected


def test_format_ast():
    assert lox.format_ast(
        lox.BinaryExpr(
            operator=lox.Token(
                token_type=lox.Plus(),
                lexeme="+",
                literal=None,
                line=1,
            ),
            left=lox.UnaryExpr(
                operator=lox.Token(
                    token_type=lox.Minus(),
                    lexeme="-",
                    literal=None,
                    line=1,
                ),
                right=lox.LiteralExpr(1),
            ),
            right=lox.LiteralExpr(2),
        )
    ) == "(+ (- 1) 2)"

    assert lox.format_ast(
        lox.BinaryExpr(
            lox.UnaryExpr(
                lox.Token(lox.Minus, "-", None, 1),
                lox.LiteralExpr(123),
            ),
            lox.Token(lox.Star, "*", None, 1),
            lox.GroupingExpr(lox.LiteralExpr(45.67)),
        )
    ) == "(* (- 123) (group 45.67))"
