from model.mainParser import DEFINED_VARS, SCOPE
import model.utils as u

def parseClosePar():
    global SCOPE
    if SCOPE.pop() != "BLOCK":
        u.SyntaxError("')' inesperado.")


def parseCloseRep(closeParToken: str):
    global SCOPE
    if closeParToken != ")":
        u.SyntaxError("Se esperaba ')' y se recibió " + closeParToken)

    if SCOPE.pop() != "REPEAT":
        u.SyntaxError("'])' inesperado.")
    

def parseCloseBra():
    global SCOPE
    if SCOPE.pop() != "IF":
        u.SyntaxError("']' inesperado.")


def parseCloseTo():
    global SCOPE
    global DEFINED_VARS
    if SCOPE.pop() != "TO":
        u.SyntaxError("'END' inesperado")
    toDel = []
    for var in DEFINED_VARS:
        if u.match("^:(.)*$", var):
            toDel.append(var)
    for var in toDel:
        DEFINED_VARS.pop(var)
    


