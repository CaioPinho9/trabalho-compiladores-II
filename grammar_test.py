import pytest

from grammar import parse

# Token constants
PLUS, MINUS, TIMES, DIV, LT, LTE, GT, GTE, EQ, NEQ, INT, NUM, OPEN, CLOSE, SEMICOLON, COMMA, ID, ASSIGN, DEF, PRINT, RETURN, IF, ELSE, LBRACE, RBRACE = \
    '+', '-', '*', '/', '<', '<=', '>', '>=', '==', '!=', 'int', 'num', '(', ')', ';', ',', 'id', '=', 'def', 'print', 'return', 'if', 'else', '{', '}'

# ---------------------
# Valid test cases
# ---------------------
@pytest.mark.parametrize("tokens", [
    # EMPTY MAIN (epsilon)
    [],

    # Single statement
    # int id;
    [INT, ID, SEMICOLON],

    # Assignment with expression
    # id = num + num;
    [ID, ASSIGN, NUM, PLUS, NUM, SEMICOLON],

    # Assignment with function call
    # id = id(id,id);
    [ID, ASSIGN, ID, OPEN, ID, COMMA, ID, CLOSE, SEMICOLON],

    # Print statement
    # print num;
    [PRINT, NUM, SEMICOLON],

    # Return statement
    # return id;
    [RETURN, ID, SEMICOLON],
    # return;
    [RETURN, SEMICOLON],

    # If statement with else
    # if (num < num) { int id; } else { print num; }
    [IF, OPEN, NUM, LT, NUM, CLOSE, LBRACE, INT, ID, SEMICOLON, RBRACE,
     ELSE, LBRACE, PRINT, NUM, SEMICOLON, RBRACE],

    # If statement without else
    # if (num > num) { return id; }
    [IF, OPEN, NUM, GT, NUM, CLOSE, LBRACE, RETURN, SEMICOLON, RBRACE],

    # Block of statements
    # { int id; int id; }
    [LBRACE, INT, ID, SEMICOLON, RETURN, SEMICOLON, RBRACE],

    # Function definition with params and statements
    # def id(int id, int id) { return id; }
    [DEF, ID, OPEN, INT, ID, COMMA, INT, ID, CLOSE, LBRACE, RETURN, SEMICOLON, RBRACE],

    # Function definition with no parameters
    # def id() { return id; }
    [DEF, ID, OPEN, CLOSE, LBRACE, RETURN, SEMICOLON, RBRACE],

    # Full program: multiple functions
    # def id() { return; } def id(int id) { int id; }
    [DEF, ID, OPEN, CLOSE, LBRACE, RETURN, SEMICOLON, RBRACE,
     DEF, ID, OPEN, INT, ID, CLOSE, LBRACE, INT, ID, SEMICOLON, RBRACE]
])
def test_valid_programs(tokens):
    assert parse(tokens) == True


# ---------------------
# Invalid test cases
# ---------------------
@pytest.mark.parametrize("tokens", [
    # Missing semicolon
    [INT, ID],

    # Invalid assignment (no expression)
    [ID, ASSIGN, SEMICOLON],

    # Function without body
    [DEF, ID, OPEN, CLOSE, LBRACE, RBRACE],

    # Missing closing parenthesis in if
    [IF, OPEN, NUM, LT, NUM, LBRACE, RETURN, SEMICOLON, RBRACE],

    # Unclosed function call
    [ID, ASSIGN, ID, OPEN, ID, SEMICOLON],

    # Invalid token sequence
    [RETURN, RETURN, RETURN],

    # Mismatched braces
    [LBRACE, INT, ID, SEMICOLON],

    # Invalid expression
    [ID, ASSIGN, NUM, PLUS, CLOSE, SEMICOLON],
])
def test_invalid_programs(tokens):
    assert parse(tokens) == False
