"""
Este modulo perime analizar la sitaxis de cadenas de tipo (BLOCK <commands>).
Las cadenas de este tipo comienzan con '(BLOCK' y terminan con ')'.
<commands> son cadenas de comandos, separadas por \\n.
"""
from model.mainParser import SCOPE
from model.mainParser import DEFINED_VARS
from model.mainParser import DEFINED_FUNCS
import model.utils as u
import model.dataStr.lists as lt
import model.tipos as ty
import model.lineCmdParse as lc


def parseBlock():
    """
    Cambia el scope a block.
    """
    global SCOPE
    SCOPE.push("BLOCK")


def parseRepeat(nParam: str, openBracket: str):
    """
    Cambia el scope a repeat, y revisa que el parámetro n de un comando REPEAT sea
    sintácticamente correcto. También revisa que el openBreacket sea de la forma '['

    Args
    ----
    nParam: str -- parámetro n. Debe ser un número entero sin signo o una variable
    previamente definida.
    nParam: str -- token correspondiente al '[' de apertura.
    """
    if not ty.isN(nParam):
        u.SyntaxError("El parámetro n de un comando REPEAT debe ser un número entero sin signo o \
            una variable previamente definida. " + nParam + " no cumple con esas condiciones.")
    if openBracket != "[":
        u.SyntaxError("Se esperaba '['. Por el contrario se recibió " + openBracket)
    global SCOPE
    SCOPE.push("REPEAT")


def parseIf(exprTokens: lt.queue, openBracket: str):
    """
    Revisa que la expresión boleana de un IF sea sintacticamente correcta.
    También revisa que el openBracket sea de la forma '['. Adicionalmente,
    cambia el scope a if

    """
    firstToken = exprTokens.dequeue()
    if u.match("^((!)?BLOCKEDP)$", firstToken):
        if exprTokens.size() > 0:
            u.SyntaxError("Token inesperado " + exprTokens.dequeue())
    
    if u.match("^(!)?CHECK$", firstToken):
        if exprTokens.size() != 2:
            u.SyntaxError("CHECK recibe 2 parámetros y recibió " + exprTokens.size())
        else:
            lc.parseCheckCommand(exprTokens.dequeue(), exprTokens.dequeue())
    
    if openBracket != "[":
        u.SyntaxError("Se esperaba '[' y se recibió " + openBracket)
    
    global SCOPE
    SCOPE.push("IF")


def parseTo(paramTokens: lt.queue, funcName: str, outputToken: str):
    """
    Revisa que params tokens sea de la forma :param, y que no existan ya
    otros parametros de la forma :param. Adicionalmente revisa que
    el token correspondiente a OUTPUT, sea de la forma OUTPUT efectivamente.
    Si pasa las dos pruebas anteriores, almacena el nombre de la función y el nombre de
    las variables.
    """
    global SCOPE
    global DEFINED_FUNCS
    acceptedTokens = []

    if SCOPE.top() != None:
        u.SyntaxError("No se pueden declarar funciones dentro de un " + SCOPE.top())
    while paramTokens.size() != 0:
        token = paramTokens.dequeue()
        parseFuncParam(token)
        acceptedTokens.append(token)
    if outputToken != "OUTPUT":
        u.SyntaxError("Se esperaba OUTPUT, pero se recibió " + outputToken)
    
    DEFINED_FUNCS[funcName] = acceptedTokens
    SCOPE.push("TO")


def parseFuncParam(token: str):
    """
    Revisa que el token sea de la forma :param. También revisa que no exista ya un parámetro
    que se llama de esa manera.
    """
    global DEFINED_VARS
    global SCOPE
    if not u.match("^:(.)*$", token):
        u.SyntaxError("Se esperaba un parámetro de la forma :param, pero se recibió " + token)
    if token in DEFINED_VARS:
        u.SyntaxError("No se pueden declarar dos parámetros con el mismo nombre: " + token)

    DEFINED_VARS[token] = None
    

