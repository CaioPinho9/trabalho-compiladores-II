PLUS, MINUS, TIMES, DIV, LT, LTE, GT, GTE, EQ, NEQ, INT, NUM, OPEN, CLOSE, SEMICOLON, COMMA, ID, ASSIGN, DEF, PRINT, RETURN, IF, ELSE, LBRACE, RBRACE = '+', '-', '*', '/', '<', '<=', '>', '>=', '==', '!=', 'int', 'num', '(', ')', ';', ',', 'id', '=', 'def', 'print', 'return', 'if', 'else', '{', '}'

next_tokens = []
next_pos = 0


def peek():
    if next_pos < len(next_tokens):
        return next_tokens[next_pos]
    return None


def has_term(tok):
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
            flist1() or
            (next_pos := save, flist2())[1]
    )


def flist1():
    return fdef() and flist()


def flist2():
    return fdef()


def fdef():
    return has_term(DEF) and has_term(ID) and has_term(OPEN) and parlist() and has_term(CLOSE) and has_term(LBRACE) and stmtlist() and has_term(RBRACE)


def parlist():
    global next_pos
    save = next_pos
    return (
            parlist1() or
            (next_pos := save, parlist2())[1] or
            True  # epsilon
    )


def parlist1():
    return has_term(INT) and has_term(ID) and has_term(COMMA) and parlist()


def parlist2():
    return has_term(INT) and has_term(ID)


def varlist():
    global next_pos
    save = next_pos
    return (
            varlist1() or
            (next_pos := save, varlist2())[1]
    )


def varlist1():
    return has_term(ID) and has_term(COMMA) and varlist()


def varlist2():
    return has_term(ID)


def stmt():
    global next_pos
    save = next_pos

    return (
            stmt1() or
            (next_pos := save, stmt2())[1] or
            (next_pos := save, stmt3())[1] or
            (next_pos := save, stmt4())[1] or
            (next_pos := save, stmt5())[1] or
            (next_pos := save, stmt6())[1] or
            (next_pos := save, stmt7())[1]
    )


def stmt1():
    return has_term(INT) and varlist() and has_term(SEMICOLON)


def stmt2():
    return atribst() and has_term(SEMICOLON)


def stmt3():
    return printst() and has_term(SEMICOLON)


def stmt4():
    return returnst() and has_term(SEMICOLON)


def stmt5():
    return ifstmt()


def stmt6():
    return has_term(LBRACE) and stmtlist() and has_term(RBRACE)


def stmt7():
    return has_term(SEMICOLON)


def atribst():
    global next_pos
    save = next_pos
    return (
            atribst1() or
            (next_pos := save, atribst2())[1]
    )


def atribst1():
    return has_term(ID) and has_term(ASSIGN) and expr()


def atribst2():
    return has_term(ID) and has_term(ASSIGN) and fcall()


def fcall():
    return has_term(ID) and has_term(OPEN) and parlistcall() and has_term(CLOSE)


def parlistcall():
    global next_pos
    save = next_pos
    return (
            parlistcall1() or
            (next_pos := save, parlistcall2())[1] or
            True  # epsilon
    )


def parlistcall1():
    return has_term(ID) and has_term(COMMA) and parlistcall()


def parlistcall2():
    return has_term(ID)


def printst():
    return has_term(PRINT) and expr()


def returnst():
    global next_pos
    save = next_pos
    return (
            returnst1() or
            (next_pos := save, returnst2())[1]
    )


def returnst1():
    return has_term(RETURN) and has_term(ID)


def returnst2():
    return has_term(RETURN)


def ifstmt():
    global next_pos
    save = next_pos
    return (
            ifstmt1() or
            (next_pos := save, ifstmt2())[1]
    )


def ifstmt1():
    return has_term(IF) and has_term(OPEN) and expr() and has_term(CLOSE) and has_term(LBRACE) and stmt() and has_term(RBRACE) and has_term(ELSE) and has_term(
        LBRACE) and stmt() and has_term(RBRACE)


def ifstmt2():
    return has_term(IF) and has_term(OPEN) and expr() and has_term(CLOSE) and has_term(LBRACE) and stmt() and has_term(RBRACE)


def stmtlist():
    global next_pos
    save = next_pos
    return (
            stmtlist1() or
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
            expr1() or
            (next_pos := save, expr2())[1] or
            (next_pos := save, expr3())[1] or
            (next_pos := save, expr4())[1] or
            (next_pos := save, expr5())[1] or
            (next_pos := save, expr6())[1] or
            (next_pos := save, numexpr())[1]
    )


def expr1():
    return numexpr() and has_term(LT) and numexpr()


def expr2():
    return numexpr() and has_term(LTE) and numexpr()


def expr3():
    return numexpr() and has_term(GT) and numexpr()


def expr4():
    return numexpr() and has_term(GTE) and numexpr()


def expr5():
    return numexpr() and has_term(EQ) and numexpr()


def expr6():
    return numexpr() and has_term(NEQ) and numexpr()


def numexpr():
    return has_term(term) and numexpr_()


def numexpr_():
    global next_pos
    save = next_pos
    return (
            numexpr_1() or
            (next_pos := save, numexpr_2())[1] or
            True  # epsilon
    )


def numexpr_1():
    return has_term(PLUS) and has_term(term) and numexpr_()


def numexpr_2():
    return has_term(MINUS) and has_term(term) and numexpr_()


def term():
    return factor() and term_()


def term_():
    global next_pos
    save = next_pos
    return (
            term_1() or
            (next_pos := save, term_2())[1] or
            True  # epsilon
    )


def term_1():
    return has_term(TIMES) and factor() and term_()


def term_2():
    return has_term(DIV) and factor() and term_()


def factor():
    global next_pos
    save = next_pos
    return (
            has_term(NUM) or
            (next_pos := save, has_term(OPEN) and numexpr() and has_term(CLOSE))[1] or
            (next_pos := save, has_term(ID))[1]
    )


def parse(tokens):
    global next_tokens, next_pos
    next_tokens = tokens
    next_pos = 0
    result = main()
    return result and next_pos == len(next_tokens)
