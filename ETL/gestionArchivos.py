import os
import urllib.request
from pyunpack import Archive



class GestionArchivos():
    RUTA_ENTRADA=None
    RUTA_SALIDA_CSV=None
    
    NOMBRE_ARCHIVO_BUQUES="buques_list.csv"
    
    def __init__(self):
        print("Gestionando Archivos")

    
    