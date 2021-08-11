from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import *

class ParseError(Exception):
    pass


@dataclass
class LeftParen:
    pass

@dataclass
class RightParen:
    pass


@dataclass
class LeftBrace:
    pass


@dataclass
class RightBrace:
    pass


@dataclass
class Comma:
    pass


@dataclass
class Dot:
    pass


@dataclass
class Minus:
    pass


@dataclass
class Plus:
    pass


@dataclass
class Semicolon:
    pass


@dataclass
class Slash:
    pass


@dataclass
class Star:
    pass


@dataclass
class Bang:
    pass


@dataclass
class BangEqual:
    pass


@dataclass
class Equal:
    pass


@dataclass
class DoubleEqual:
    pass


@dataclass
class Greater:
    pass


@dataclass
class GreaterEqual:
    pass


@dataclass
class Less:
    pass


@dataclass
class LessEqual:
    pass

@dataclass
class Identifier:
    pass


@dataclass
class String:
    pass


@dataclass
class Number:
    pass


@dataclass
class AndToken:
    pass


@dataclass
class ClassToken:
    pass


@dataclass
class ElseToken:
    pass


@dataclass
class FalseToken:
    pass


@dataclass
class FunToken:
    pass


@dataclass
class ForToken:
    pass


@dataclass
class IfToken:
    pass


@dataclass
class NilToken:
    pass


@dataclass
class OrToken:
    pass


@dataclass
class PrintToken:
    pass


@dataclass
class ReturnToken:
    pass


@dataclass
class SuperToken:
    pass


@dataclass
class ThisToken:
    pass


@dataclass
class TrueToken:
    pass


@dataclass
class VarToken:
    pass


@dataclass
class WhileToken:
    pass


@dataclass
class EndOfFile:
    pass



TokenType = Union[
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    Comma,
    Dot,
    Minus,
    Plus,
    Semicolon,
    Slash,
    Star,
    Bang,
    BangEqual,
    Equal,
    DoubleEqual,
    Greater,
    GreaterEqual,
    Less,
    LessEqual,
    Identifier,
    String,
    Number,
    AndToken,
    ClassToken,
    ElseToken,
    TrueToken,
    FalseToken,
    FunToken,
    ForToken,
    IfToken,
    NilToken,
    OrToken,
    PrintToken,
    ReturnToken,
    SuperToken,
    ThisToken,
    VarToken,
    WhileToken,
    EndOfFile,
]

@dataclass
class Token:
    token_type: TokenType
    lexeme: str = field(default=None, compare=False)
    literal: Any = field(default=None)
    line: int = field(default=-1, compare=False)

    def __str__(self):
        return f"{self.token_type} {lexeme} {literal}"


Operator = Union[DoubleEqual, BangEqual]


@dataclass
class Expr:
    pass


@dataclass
class LiteralExpr(Expr):
    value: Any


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Token
    right: Expr


@dataclass
class GroupingExpr(Expr):
    expression: Expr


@dataclass
class VariableExpr(Expr):
    name: Token


@dataclass
class AssignExpr(Expr):
    name: Token
    value: Expr


class Statement:
    pass


@dataclass
class VariableStatement(Statement):
    name: Token
    initializer: Expr


@dataclass
class ExpressionStatement(Statement):
    expression: Expr


@dataclass
class PrintStatement(Statement):
    expression: Expr

@dataclass
class BlockStatement(Statement):
    statements: list[Statement]


@dataclass
class Scanner:
    source: str
    tokens: list[Token] = field(default_factory=list)
    start: int = 0
    current: int = 0
    line: int = 1

    @classmethod
    def scan_str(cls, input_str):
        scanner = cls(input_str)
        return scanner.scan_tokens()

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(
            Token(
                token_type = EndOfFile(),
                lexeme = "",
                literal = None,
                line = self.line,
            )
        )
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(LeftParen())
            case ")":
                self.add_token(RightParen())
            case "{":
                self.add_token(LeftBrace())
            case "}":
                self.add_token(RightBrace())
            case ",":
                self.add_token(Comma())
            case ".":
                self.add_token(Dot())
            case "-":
                self.add_token(Minus())
            case "+":
                self.add_token(Plus())
            case ";":
                self.add_token(Semicolon())
            case "*":
                self.add_token(Star())
            case "!":
                self.add_token(BangEqual() if self.match("=") else Bang())
            case "=":
                self.add_token(DoubleEqual() if self.match("=") else Equal())
            case "<":
                self.add_token(LessEqual() if self.match("=") else Less())
            case ">":
                self.add_token(GreaterEqual() if self.match("=") else Greater())
            case "/":
                if self.match("/"):
                    # Consume the rest of the line of this comment
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(Slash())
            case "\n":
                # Keep track of line number for reporting purposes
                self.line += 1
                pass
            case " " | "\r" | "\t":
                # Ignore non-newline whitespace
                pass
            case '"':
                self.string()
            case c if c.isdigit():
                self.number()
            case c if c.isalpha():
                self.identifier()
            case _:
                Lox.error(self.line, f"Unexpected character {repr(c)}")

    def match(self, expected) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        # Consume the character if it matches
        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current+1]

    def string(self):
        starting_line = self.line
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            Lox.error(line, "Unterminated string on line {starting_line}")
            return

        self.advance()
        value = self.source[self.start+1:self.current-1]
        self.add_token(String(), value)

    def number(self):
        while True:
            if self.peek().isdigit():
                self.advance()
            else:
                break

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while True:
                if self.peek().isdigit():
                    self.advance()
                else:
                    break

        self.add_token(Number(), float(self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        keyword_tokens = {
            "and": AndToken(),
            "class": ClassToken(),
            "else": ElseToken(),
            "false": FalseToken(),
            "for": ForToken(),
            "fun": FunToken(),
            "if": IfToken(),
            "nil": NilToken(),
            "or": OrToken(),
            "print": PrintToken(),
            "return": ReturnToken(),
            "super": SuperToken(),
            "this": ThisToken(),
            "true": TrueToken(),
            "var": VarToken(),
            "while": WhileToken(),
        }

        text = self.source[self.start:self.current]
        self.add_token(keyword_tokens.get(text, Identifier()))

    def scan_source(self):
        raise NotImplementedError

    def add_token(self, token_type: TokenType, literal: Any = None):
        text = self.source[self.start:self.current]
        self.tokens.append(
            Token(
                token_type = token_type,
                lexeme = text,
                literal = literal,
                line = self.line,
            )
        )

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)


def print_ast(expression: Expr):
    print(format_ast(expression))


def format_ast(expr: Expr):
    match expr:
        case LiteralExpr():
            if expr.value is None:
                return "nil"
            return str(expr.value)
        case UnaryExpr():
            return f"({expr.operator.lexeme} {format_ast(expr.right)})"
        case GroupingExpr():
            return f"(group {format_ast(expr.expression)})"
        case BinaryExpr():
            return f"({expr.operator.lexeme} {format_ast(expr.left)} {format_ast(expr.right)})"
        case _:
            assert False, f"got unexpected Expr type: {type(expr)}"


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    @classmethod
    def parse_str(cls, input_str) -> Expr:
        parser = cls(Scanner.scan_str(input_str))
        return parser.parse()

    def parse(self) -> Expr:
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())

        return statements

    def declaration(self):
        try:
            if self.match(VarToken()):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def var_declaration(self):
        token = self.consume(Identifier(), "Expect variable name")
        initializer = None
        if self.match(Equal()):
            initializer = self.expression()

        self.consume(Semicolon(), "Expect ';' after variable declaration")
        return VariableStatement(token, initializer)


    def statement(self):
        if self.match(PrintToken()):
            return self.print_statement()
        if self.match(LeftBrace):
            return BlockStatement(self.block_statement())
        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(Semicolon(), "Expect ';' after value")
        return PrintStatement(value)

    def expression_statement(self):
        value = self.expression()
        self.consume(Semicolon(), "Expect ';' after expression")
        return ExpressionStatement(value)

    def block_statement(self) -> list[Statement]:
        statements = []
        while not self.check(RightBrace()) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(RightBrace(), "Expect '}' after block.")
        return statements

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(Equal()):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, VariableExpr):
                name = expr.name
                return AssignExpr(name, value)

            self.error(equals, "Invalid assignment target")

        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(BangEqual(), DoubleEqual()):
            operator = self.previous()
            right = self.comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()
        while self.match(Greater(), GreaterEqual(), Less(), LessEqual()):
            operator = self.previous()
            right = self.term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def term(self):
        expr = self.factor()
        while self.match(Minus(), Plus()):
            operator = self.previous()
            right = self.factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()
        while self.match(Slash(), Star()):
            operator = self.previous()
            right = self.unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def unary(self):
        if self.match(Bang(), Minus()):
            operator = self.previous()
            right = self.unary()
            return UnaryExpr(operator, right)

        return self.primary()

    def primary(self):
        token = self.advance()
        match token.token_type:
            case FalseToken():
                return LiteralExpr(False)
            case TrueToken():
                return LiteralExpr(True)
            case NilToken():
                return LiteralExpr(None)
            case Number() | String():
                return LiteralExpr(token.literal)
            case LeftParen():
                expr = self.expression()
                self.consume(RightParen(), "Expected ')' after expression.")
                return GroupingExpr(expr)
            case Identifier():
                return VariableExpr(token)
            case _:
                #breakpoint()
                raise self.error(self.peek(), "Expected expression")

    def match(self, *token_types: Token) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True

        return False

    def check(self, token_type: Token) -> bool:
        if self.is_at_end():
            return False
        return self.peek().token_type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().token_type == EndOfFile()

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def consume(self, token_type, message: str):
        if self.check(token_type):
            return self.advance()

        #breakpoint()
        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        Lox.error_token(token, message)
        return ParseError("parse error")

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous.token_type == Semicolon:
                return

            match self.peek().token_type:
                case ClassToken() | ForToken() | FunToken() | IfToken() | PrintToken() | ReturnToken() | VarToken() | WhileToken():
                    return
                case _:
                    pass

        self.advance()


@dataclass
class Environment:
    enclosing: Optional[Environment] = None
    values: dict[str, Any] = field(default_factory=dict)

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]

        elif self.enclosing:
            return self.enclosing.get(name)

        raise Exception(f"Undefined variable {name.lexeme}.")


    def define(self, name, value):
        self.values[name.lexeme] = value

    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return value

        elif self.enclosing:
            return self.enclosing.assign(name, value)

        raise Exception(f"Undefined variable {name.lexeme}.")



@dataclass
class Interpreter:
    environment: Environment = field(default_factory=Environment)

    @classmethod
    def evaluate_str(cls, input_str):
        interpreter = cls()
        scanner = Scanner(input_str)
        parser = Parser(scanner.scan_tokens())
        return interpreter.evaluate(parser.expression())

    def interpret(self, stmts):
        try:
            for statement in stmts:
                self.execute(statement)
            #print(self.stringify(result))
        except Exception as exc:
            Lox.runtime_error(exc.args[0])

    def execute(self, stmt):
        match stmt:
            case PrintStatement():
                result = self.evaluate(stmt.expression)
                print(self.stringify(result))
            case ExpressionStatement():
                self.evaluate(stmt.expression)
            case VariableStatement():
                value = None
                if stmt.initializer:
                    value = self.evaluate(stmt.initializer)
                self.environment.define(stmt.name, value)
            case _:
                #breakpoint()
                raise Exception(f"Unexpected statement {stmt}")

    def evaluate(self, expr: Expr):
        match expr:
            case LiteralExpr():
                return expr.value

            case UnaryExpr(operator=Token(token_type=Minus())):
                return -self.evaluate(expr.right)

            case UnaryExpr(operator=Token(token_type=Bang())):
                return not self.is_truthy(self.evaluate(expr.right))

            case GroupingExpr():
                return self.evaluate(expr.expression)

            case VariableExpr():
                return self.environment.get(expr.name)

            case AssignExpr():
                value = self.evaluate(expr.value)
                self.environment.assign(expr.name, value)
                return value

            case BinaryExpr():
                left = self.evaluate(expr.left)
                right = self.evaluate(expr.right)
                match expr.operator.token_type, left, right:
                    case Minus(), float(), float():
                        return left - right

                    case Slash(), float(), float():
                        return left / right

                    case Star(), float(), float():
                        return left * right

                    case Greater(), float(), float():
                        return left > right

                    case GreaterEqual(), float(), float():
                        return left >= right

                    case Less(), float(), float():
                        return left < right

                    case LessEqual(), float(), float():
                        return left <= right

                    case Plus(), float(), float():
                        return left + right

                    case Plus(), str(), str():
                        return left + right

                    case BangEqual(), _, _:
                        return not self.is_equal(left, right)

                    case DoubleEqual(), _, _:
                        return self.is_equal(left, right)

                    case _:
                        raise Exception(f"Operand '{expr.operator.lexeme}' not supported between {type(left).__name__} and {type(right).__name__} on line {expr.operator.line}")

            case _:
                #breakpoint()
                raise Exception(f"Unexpected expression {expr}")

    @staticmethod
    def is_equal(left, right):
        # This may get more complicated later?
        return left == right

    @staticmethod
    def is_truthy(value) -> bool:
        match value:
            case bool():
                return value
            case None:
                return False
            case _:
                return True

    @staticmethod
    def stringify(value):
        match value:
            case None:
                return 'nil'
            case True:
                return 'true'
            case False:
                return 'false'
            case float():
                # Remove the trailing the ".0" so that ints looks like ints
                text = str(value).removesuffix('.0')
                return text
            case _:
                return str(value)


_had_error = False
_had_runtime_error = False
@dataclass
class Lox:
    interpreter: Interpreter = field(default_factory=Interpreter)

    @staticmethod
    def get_error(_):
        global _had_error
        return _had_error

    @staticmethod
    def set_error(_, val):
        global _had_error
        _had_error = val

    # TODO: how to do classproperties like java statics? Not that I think that's
    # good, but that's how the book does it.
    had_error = property(get_error, set_error)

    @staticmethod
    def get_runtime_error(_):
        global _had_runtime_error
        return _had_runtime_error

    @staticmethod
    def set_runtime_error(_, val):
        global _had_runtime_error
        _had_runtime_error = val

    # TODO: how to do classproperties like java statics? Not that I think that's
    # good, but that's how the book does it.
    had_runtime_error = property(get_runtime_error, set_runtime_error)

    def run_file(self, path: Path | str):
        with open(path) as f:
            source = f.read()
        self.run(source)

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)


    def run_prompt(self):
        while True:
            try:
                line = input("> ")
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            self.run(line)

            # If the user is running interactively, an error shouldn't kill the
            # entire session.
            self.had_error = False

    def run(self, source: str):
        self.interpreter.interpret(Parser.parse_str(source))


    @classmethod
    def error(cls, line: int, message: str):
        cls.report(line, "", message)

    @classmethod
    def runtime_error(cls, message):
        print(
            message,
            file=sys.stderr
        )
        cls.had_runtime_error = True

    @classmethod
    def error_token(cls, token, message):
        if token.token_type == EndOfFile():
            cls.report(token.line, " at end", message)
        else:
            cls.report(token.line, " at '" + token.lexeme + "'", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print(
            f"[line {line}] Error {where}: {message}",
            file=sys.stderr
        )

        cls.had_error = True


def main(args):
    if len(args) > 1:
        print("Usage: lox.py [script]", file=sys.stderr)
        sys.exit(64)
    elif args:
        script_file = args[0]
        Lox().run_file(script_file)
    else:
        Lox().run_prompt()
