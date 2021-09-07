"""
Este modulo analiza la sintaxis de las cadenas de tipo comando. Las cadenas de tipo
comando  deben estar contenidas en una sola linea, y sus tokens se separan por los espacios.

El metodo parseCommand recibe una cadena con 1 comando y retorna True
si el comando es sintacticamente correcto, o False de lo contrario.
"""
from model.mainParser import DEFINED_VARS, SCOPE
import model.tipos as ty
import model.utils as u

def parseNCommand(nParam: str):
    """
    Revisa si un comando de tipo n es sintacticamente correcto.
    Un comando de tipo n, es aquel que solo recive un parametro (n).
    n es un número o una variable numerica definida previamente.

    Args
    ----
    instrucción: str --  comando (ej: MOVE)
    nParam: str -- parametro o

    Returns
    -------
    bool -- True si es sintacticamente correcto o False de lo contrario.
    """
    # Revisa que el parámetro sea de tipo n
    if not ty.isN(nParam): u.SyntaxError(nParam + " no es un número o una variable previamente definida")
    return



def parseLookCommand(OParam: str):

    """
    Revisa si un comando de tipo LOOK es sintacticamente correcto.
    Un comando de tipo LOOK, recibe un solo parametro (O).
    O es un caracter (N|E|W|S).

    Args
    ----
    OParam: str -- Parametro de tipo O
    """
    # Revisa que el segundo token sea O
    if not u.match("^(N|E|W|S)$", OParam): u.SyntaxError("Parámetro " + OParam + " de tipo erroneo.\
        El parámetro del comando 'LOOK' debe ser 'N', 'E' 'W' o 'S'.")

def parseCheckCommand(OParam: str, nParam: str):
    """
    Revisa si un comando de tipo CHECK es sintacticamente correcto.
    Un comando de tipo CHECK, recibe 2 parametros (O, n), y es de la forma CHECK O n
    O es un caracter (C|B). n es un número entero sin signo.

    Args
    ----
    OPara: str -- parámetro O
    nPara: str -- parámetro n
    """
    if not u.match("^(C|B)$", OParam):
        u.SyntaxError("Parámetro " + OParam + " de tipo erroneo. El parámetro O del comando \
            'CHECK' debe ser 'C' o 'B'.")
    if not ty.isN(nParam):
        u.SyntaxError(nParam + "no es un número o una variable preciamente definida")


def parseDefineCommand(nParam: str, valParam: str):
    """
    Revisa que un comando de tipo Define sea sintácticamente correcto.
    Si la declaración es sintacticamente correcta, añade la variable al mapa de variables
    definidas. Adicionalmente, revisa que la variable no sea definida en un scope diferente a
    global.

    Args
    ----
    nParam: str -- Nombre de la variable a definir. Debe ser toda en minuscula
    valParam: str -- Valor a asignar. Debe ser un entero sin signo.
    """
    global DEFINED_VARS
    global SCOPE

    if SCOPE.top() != None:
        u.SyntaxError("No se pueden definir variables dentro de un " + SCOPE.top())
    elif not nParam.islower():
        u.SyntaxError("El nombre de variable " + nParam + " debe ser en minúscula.")
    elif not ty.isPositiveInt(valParam):
        u.SyntaxError("El valor " + valParam + " asignado a la variable " + nParam + " debe ser un entero sin signo.")
    else:
        DEFINED_VARS[nParam] = valParam


def parseFuncCall(params: list):
    for param in params:
        if not ty.isN(param):
            u.SyntaxError(param + " no es un número entero o una variable previamente definida.")