"""
Este modulo analiza la sintaxis de las cadenas de tipo comando.

El metodo parseCommand recibe una cadena con 1 comando y retorna True
si el comando es sintacticamente correcto, o False de lo contrario.
"""
import re
import tipos as ty
import utils as u

# Almacena el scope actual del codigo
def parseCommand(command: str):
    """
    Revisa si un command es sintacticamente correcto.

    Args
    ----
    command: str -- Comando a revisar

    Returns
    -------
    bool -- True si pasa el parse, False de lo contrario
    """
    # Elimina espacios en los extremos
    command = command.strip()
    # Separa la linea en un array, en cada espacio
    tokens = command.split()
    # Posibles opciones de comienzo de linea
    if u.match("^(MOVE|RIGHT|LEFT|ROTATE|DROP|FREE|PICK|POP)$", tokens[0]):
        return parseNCommand(tokens)
    elif u.match("^(LOOK)$", tokens[0]):
        return parseLookCommand(tokens)
    elif u.match("^(CHECK)$", tokens[0]):
        return parseCheckCommand(tokens)
    elif u.match("^(BLOCKEDP|NOP)", tokens[0]):
        return parseNACommand(tokens)
    else:
        return False


def parseNCommand(tokens: list):
    """
    Revisa si un comando de tipo n es sintacticamente correcto.
    Un comando de tipo n, es aquel que solo recive un parametro (n).
    n es un número o una variable numerica definida previamente.

    Args
    ----
    tokens: list -- lista con los tokens del comando.

    Returns
    -------
    bool -- True si es sintacticamente correcto o False de lo contrario.
    """
    # Revisa si el comando tiene solo 2 tokens. El primero debe corresponder al comando, y el segundo a n.
    if len(tokens) != 2:
        return False
    # Revisa que el segundo token sea n.
    elif not ty.isN(tokens[1]):
        return False
    else:
        return True


def parseLookCommand(tokens: list):

    """
    Revisa si un comando de tipo LOOK es sintacticamente correcto.
    Un comando de tipo LOOK, recibe un solo parametro (O).
    O es un caracter (N|E|W|S).

    Args
    ----
    tokens: list -- lista con los tokens del comando.

    Returns
    -------
    bool -- True si es sintacticamente correcto o False de lo contrario.
    """
    # Revisa si tokens, solo contiene 2 tokens.
    if len(tokens) != 2:
        return False
    # Revisa que el segundo token sea O
    if not u.match("^(N|E|W|S)$", tokens[1]):
        return False
    
    return True


def parseCheckCommand(tokens: list):
    """
    Revisa si un comando de tipo CHECK es sintacticamente correcto.
    Un comando de tipo CHECK, recibe 2 parametros (O, n), y es de la forma CHECK O n
    O es un caracter (C|B). n es un número entero sin signo.

    Args
    ----
    tokens: list -- lista con los tokens del comando.

    Returns
    -------
    bool -- True si es sintacticamente correcto o False de lo contrario.
    """
    # Revisa que tokens tenga solo 3 tokens
    if len(tokens) != 3:
        return False
    # Revisa que el segundo token sea O
    if not u.match("^(C|B)$", tokens[1]):
        return False
    # Revisa que el tercer token sea n
    if not ty.isPositiveInt(tokens[2]):
        return False
    
    return True


def parseNACommand(tokens):
    """
    Revisa si un comando es de tipo NOP o BLOCKEDP.
    Ambos comandos no reciben parámetros, por lo que solo deben contener 1 token.

    
    Args
    ----
    tokens: list -- lista con los tokens del comando.

    Returns
    -------
    bool -- True si es sintacticamente correcto o False de lo contrario.
    """
    if len(tokens) != 1:
        return False
    
    return True