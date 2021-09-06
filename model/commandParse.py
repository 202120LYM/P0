from model.dataStr.lists import queue
import re
import utils as u
import lineCmdParse as lcp
import dataStr.lists as lt
import containerParse as cp
import clousersParse as clop
from main import SCOPE

def CommandParse(tokensLst: list):
    """
    Revisa que un comando en forma de tokens sea sintacticamente correcto. Termina de revisar cuando
    no quedan mas tokens

    Args
    ----
    tokens: list -- lista de tokens
    """
    global SCOPE
    tokens = lt.tokens(tokensLst)
    # Ciclo por los tokens
    while tokens.size() != 0:
        token = tokens.dequeue()
        if u.match("^(MOVE|RIGHT|LEFT|ROTATE|DROP|FREE|PICK|POP)$", token):
            # Revisa que cumpla la sintaxis
            lcp.parseNCommand(tokens.dequeue())
        elif u.match("^(LOOK)$", token):
            lcp.parseLookCommand(tokens.dequeue())
        elif u.match("^(CHECK)$", token):
            lcp.parseCheckCommand(tokens.dequeue(), tokens.dequeue())
        elif u.match("^(BLOCKEDP|NOP)$", token):
            continue
        elif u.match("^(DEFINE)$"):
            lcp.parseDefineCommand(tokens.dequeue(), tokens.dequeue())
        elif u.match("^(\(BLOCK)$"):
            cp.parseBlock()
        elif u.match("^(\(REPEAT)$", token):
            cp.parseRepeat(tokens.dequeue())
        elif u.match("^(IF)$"):
            ifTokens = lt.queue()
            while token != "[":
                token = tokens.dequeue()
                ifTokens.enqueue(token)
            cp.parseIf(ifTokens, token)
        elif u.match("^(TO)$"):
            paramTokens = lt.queue()
            token = tokens.dequeue()
            while u.match("^:(.)*$", token):
                paramTokens.enqueue(token)
                token = tokens.dequeue()
            cp.parseTo(paramTokens, token, tokens.dequeue())
        elif u.match("^\)$", token):
            clop.parseClosePar()
        elif u.match("^\]$", token):
            if SCOPE.top() == "REPEAT":
                clop.parseCloseRep(tokens.dequeue())
            else:
                clop.parseCloseBra()
        elif u.match("^END$"):
            clop.parseCloseTo()
    
    if SCOPE.top != None:
        u.SyntaxError("Fin del archivo inesperado.")
        


def splitCommand(command: str):
    """
    Separa la cadena en tokens. No revisa que los tokens sean correctos.

    Args
    ----
    commands: str -- comando a revisar

    Returns
    -------
    bool -- Trues si es correcto o False de lo contrario
    """
    # Da formato antes y después de los separadores
    command = formatArroundSeparators(command)
    # Separa la cadena en los espacios
    tokens = command.split("")

    return tokens


def formatArroundSeparators(command: str):
    """
    Añade los espacios correctos antes y despúes de los separadores.
    Se leen como separadores: ' ', '(', ')', ':', '[', ']'

    Args
    ----
    commands: str -- cadena a modificar

    Returns
    -------
    Cadena commands sin espacios antes y despúes de separadores.
    """
    patterns = {
        "((\s)*)\(((\s)*)": " (",
        "((\s)*)\)((\s)*)": " ) ",
        "((\s)*)(:)((\s)*)": " :",
        "((\s)*)\[((\s)*)": " [ ",
        "((\s)*)\]((\s)*)": " ] ",
        "((\s)*)(!)((\s)*)": " !"
    }
    
    for pattern in patterns:
        regex = re.compile(pattern)
        replace = patterns[pattern]
        command = regex.sub(replace, command)
    
    return command
    



