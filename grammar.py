PLUS, MINUS, TIMES, DIV, LT, LTE, GT, GTE, EQ, NEQ, INT, NUM, OPEN, CLOSE, SEMICOLON, COMMA, ID, ASSIGN, DEF, PRINT, RETURN, IF, ELSE, LBRACE, RBRACE = '+', '-', '*', '/', '<', '<=', '>', '>=', '==', '!=', 'int', 'num', '(', ')', ';', ',', 'id', '=', 'def', 'print', 'return', 'if', 'else', '{', '}'

next_tokens = []
next_pos = 0


def peek():
    if next_pos < len(next_tokens):
        return next_tokens[next_pos]
    return None


def term(tok):
    global next_pos
    if peek() == tok:
        next_pos += 1
        return True
    return False


def main():
    global next_pos
    save = next_pos
    if stmt():
        return True
    next_pos = save
    if expr():
        return True
    next_pos = save
    # ε case: match nothing
    return True


def flist():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, flist1())[1] or
            (next_pos := save, flist2())[1]
    )


def flist1():
    return fdef() and flist()


def flist2():
    return fdef()


def fdef():
    return term(DEF) and term(ID) and term(OPEN) and parlist() and term(CLOSE) and term(LBRACE) and stmtlist() and term(RBRACE)


def parlist():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, parlist1())[1] or
            (next_pos := save, parlist2())[1] or
            True  # epsilon
    )


def parlist1():
    return term(INT) and term(ID) and term(COMMA) and parlist()


def parlist2():
    return term(INT) and term(ID)


def varlist():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, varlist1())[1] or
            (next_pos := save, varlist2())[1]
    )


def varlist1():
    return term(ID) and term(COMMA) and varlist()


def varlist2():
    return term(ID)


def stmt():
    global next_pos
    save = next_pos

    return (
            (next_pos := save, stmt1())[1] or
            (next_pos := save, stmt2())[1] or
            (next_pos := save, stmt3())[1] or
            (next_pos := save, stmt4())[1] or
            (next_pos := save, stmt5())[1] or
            (next_pos := save, stmt6())[1] or
            (next_pos := save, stmt7())[1]
    )


def stmt1():
    return term(INT) and varlist() and term(SEMICOLON)


def stmt2():
    return atribst() and term(SEMICOLON)


def stmt3():
    return printst() and term(SEMICOLON)


def stmt4():
    return returnst() and term(SEMICOLON)


def stmt5():
    return ifstmt()


def stmt6():
    return term(LBRACE) and stmtlist() and term(RBRACE)


def stmt7():
    return term(SEMICOLON)


def atribst():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, atribst1())[1] or
            (next_pos := save, atribst2())[1]
    )


def atribst1():
    return term(ID) and term(ASSIGN) and expr()


def atribst2():
    return term(ID) and term(ASSIGN) and fcall()


def fcall():
    return term(ID) and term(OPEN) and parlistcall() and term(CLOSE)


def parlistcall():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, parlistcall1())[1] or
            (next_pos := save, parlistcall2())[1] or
            True  # epsilon
    )


def parlistcall1():
    return term(ID) and term(COMMA) and parlistcall()


def parlistcall2():
    return term(ID)


def printst():
    return term(PRINT) and expr()


def returnst():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, returnst1())[1] or
            (next_pos := save, returnst2())[1]
    )


def returnst1():
    return term(RETURN) and term(ID)


def returnst2():
    return term(RETURN)


def ifstmt():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, ifstmt1())[1] or
            (next_pos := save, ifstmt2())[1]
    )


def ifstmt1():
    return term(IF) and term(OPEN) and expr() and term(CLOSE) and term(LBRACE) and stmt() and term(RBRACE) and term(ELSE) and term(LBRACE) and stmt() and term(RBRACE)


def ifstmt2():
    return term(IF) and term(OPEN) and expr() and term(CLOSE) and term(LBRACE) and stmt() and term(RBRACE)


def stmtlist():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, stmtlist1())[1] or
            (next_pos := save, stmtlist2())[1]
    )


def stmtlist1():
    return stmt() and stmtlist()


def stmtlist2():
    return stmt()


def expr():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, expr1())[1] or
            (next_pos := save, expr2())[1] or
            (next_pos := save, expr3())[1] or
            (next_pos := save, expr4())[1] or
            (next_pos := save, expr5())[1] or
            (next_pos := save, expr6())[1] or
            (next_pos := save, numexpr())[1]
    )


def expr1():
    return numexpr() and term(LT) and numexpr()


def expr2():
    return numexpr() and term(LTE) and numexpr()


def expr3():
    return numexpr() and term(GT) and numexpr()


def expr4():
    return numexpr() and term(GTE) and numexpr()


def expr5():
    return numexpr() and term(EQ) and numexpr()


def expr6():
    return numexpr() and term(NEQ) and numexpr()


def numexpr():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, numexpr())[1] and term(PLUS) and term_() or
            (next_pos := save, numexpr())[1] and term(MINUS) and term_() or
            (next_pos := save, term_())[1]
    )


def term_():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, term_())[1] and term(TIMES) and factor() or
            (next_pos := save, term_())[1] and term(DIV) and factor() or
            (next_pos := save, factor())[1]
    )


def factor():
    global next_pos
    save = next_pos
    return (
            (next_pos := save, term(NUM))[1] or
            (next_pos := save, term(OPEN) and numexpr() and term(CLOSE))[1] or
            (next_pos := save, term(ID))[1]
    )


def parse(tokens):
    global next_tokens, next_pos
    next_tokens = tokens
    next_pos = 0
    result = main()
    return result and next_pos == len(next_tokens)
