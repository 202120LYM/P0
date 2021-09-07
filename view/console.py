import os
import sys

path = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.abspath(path))

import model.mainParser as parser


def mainProgram():
    file_path = input("Por favor ingrese la dirección del archivo a revisar:\n\t")
    while not os.path.isfile(file_path):
        print("Dirección invalida.")
        file_path = input("Por favor ingrese la dirección del archivo a revisar:\n\t")
    
    with open(file_path) as file:
        contents = file.read()
        parser.parse(contents)

        print("El archivo cumple con las condiciones sintácticas.")
        

mainProgram()