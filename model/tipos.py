from main import DEFINED_VARS
from main import SCOPE
import utils as u

def isDefinedVar(token: str):
    """
    Revisa si un token pasado por parámetro es una variable definida previamente.

    Args
    ----
    token: str -- token a revisar.

    Returns
    -------
    bool -- True si existe una variable con el nombre del token. False de lo contrario
    """
    global DEFINED_VARS
    if token in DEFINED_VARS:
        return True
    else:
        return False


def isPositiveInt(token: str):
    """
    Revisa si el token pasado por parámetro es un entero positivo.

    Args
    ----
    token: str -- token a revisar

    Returns
    -------
    bool -- True si es sitacticamente correcto, False de lo contrario.
    """
    if u.match("^([0-9])+$", token):
        return True
    else:
        return False


def isN(token: str):
    """
    Revisa si un token es de tipo n. Un token de tipo n es un número entero SIN signo
    o una variable previamente definida.
    """
    if isPositiveInt(token) or isDefinedVar(token):
        return True
    else:
        return False