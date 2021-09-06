import re

def match(regex: str, string: str):
    """
    Retorna True si regex se encuentra en string. False de lo contrario

    Args
    ----
    regex: str -- patrón. Debe ser una cadena valida para el compilador de regex
    string: str -- Cadena en la cual buscar el patrón
    """
    return (re.compile(regex).search(string) is not None)