import model.dataStr.lists as lt
if not 'SCOPE' in globals():
    SCOPE = lt.stack()
    DEFINED_VARS = {}
    DEFINED_FUNCS = {}

import re
import model.utils as u
import model.lineCmdParse as lcp
import model.containerParse as cp
import model.clousersParse as clop
import model.tipos as ty
import model.lineCmdParse as lc





def parse(fileContents: str):
    tokensLst = splitCommands(fileContents)
    CommandParse(tokensLst)


def CommandParse(tokensLst: list):
    """
    Revisa que un comando en forma de tokens sea sintacticamente correcto. Termina de revisar cuando
    no quedan mas tokens

    Args
    ----
    tokens: list -- lista de tokens
    """
    global SCOPE
    global DEFINED_FUNCS
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
        elif u.match("^(DEFINE)$", token):
            lcp.parseDefineCommand(tokens.dequeue(), tokens.dequeue())
        elif u.match("^(\(BLOCK)$", token):
            cp.parseBlock()
        elif u.match("^(\(REPEAT)$", token):
            cp.parseRepeat(tokens.dequeue())
        elif u.match("^(IF)$", token):
            ifTokens = lt.queue()
            token = tokens.dequeue()
            while token != "[":
                ifTokens.enqueue(token)
                token = tokens.dequeue()
            cp.parseIf(ifTokens, token)
        elif u.match("^(TO)$", token):
            paramTokens = lt.queue()
            funcName = tokens.dequeue()
            token = tokens.dequeue()
            while u.match("^:(.)*$", token):
                paramTokens.enqueue(token)
                token = tokens.dequeue()
            cp.parseTo(paramTokens, funcName, token)
        elif u.match("^\)$", token):
            clop.parseClosePar()
        elif u.match("^\]$", token):
            if SCOPE.top() == "REPEAT":
                clop.parseCloseRep(tokens.dequeue())
            else:
                clop.parseCloseBra()
        elif u.match("^END$", token):
            clop.parseCloseTo()
        elif token in DEFINED_FUNCS:
            params = []
            for param in DEFINED_FUNCS[token]:
                params.append(tokens.dequeue())
            lcp.parseFuncCall(params)
        else:
            u.SyntaxError("Token inesperado " + token)
    if SCOPE.top() != None:
        u.SyntaxError("Fin del archivo inesperado.")
        


def splitCommands(command: str):
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
    tokens = command.split()

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