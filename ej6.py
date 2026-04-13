# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:09:31 2026

@author: saand
"""

import os
import urllib.request
import json
from time import sleep

from threading import Thread, active_count

class HebraOrdenes(Thread):
    def __init__(self, lista, orden):
        super().__init__()
        self.lista = lista
        self.orden = orden
        
    def run(self):
        self.lista.append(self.orden)
        if self.orden.startswith("temp"):
            color_print(f"temperatura en {self.orden.split()[1]}: " + pide_temperatura(f'{self.orden.split()[1]}'), "azul")
        elif self.orden.startswith("espera"):
            color_print(f"Voy a esperar {self.orden.split()[1]} segundos.", "verde")
            espera_online(int(self.orden.split()[1]))
            color_print(f"He esperado {self.orden.split()[1]} segundos.", "verde")
            
        elif self.orden == "dato":
            dato = pide_dato_random()
            color_print("Dato random: " + dato, "amarillo")
            
        elif self.orden == "chiste":
            chiste = pide_chiste()
            color_print("Chiste: " + chiste, "morado")
            
        elif self.orden == "salir":
            print("salir")
        else:
            print("No se hace nada")
            
    
                
        


def color_print(texto: str, color: str) -> None:
    # usa códigos ANSI para escribir texto con colores en la consola
    colores = {"rojo": "\033[91m",
               "verde": "\033[92m",
               "amarillo": "\033[93m",
               "azul": "\033[94m",
               "morado": "\033[95m",
               "negro": "\033[30m"}
    reset = "\033[0m"
    print(f"{colores[color]}{texto}{reset}")

def espera_online(duracion: int) -> None:
    # Espera el tiempo que se diga usando un servicio online.
    with urllib.request.urlopen(f"https://httpbin.org/delay/{duracion}") as response:
        response.read()

def pide_chiste() -> str:
    # Devuelve el texto de un chiste aleatorio.
    url = "https://official-joke-api.appspot.com/random_joke"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
    return f"{data['setup']} {data['punchline']}"

def pide_dato_random() -> str:
    # Devuelve el texto de un dato curioso aleatorio.
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode('utf-8'))
    return data['text']

def pide_temperatura(ciudad: str) -> str:
    # Devuelve (como texto) la temperatura actual de la ciudad dada.
    # Este servicio puede ser muy lento en contestar, y puede fallar.
    url = f"https://wttr.in/{ciudad}?format=%t"
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8').strip()

def vigila(filename: str) -> None:
    # Imprime el contenido del archivo vigilado cada vez que se modifica.
    existe_arch = True
    contenido_ant = ""
    while existe_arch:
        with open(filename, 'r') as arch:
            contenido_act = arch.read()
            if contenido_act != contenido_ant:
                color_print(f"Contenido del archivo vigilado: \n{contenido_act}\n", "morado")
                contenido_ant = contenido_act
        sleep(1)
        if not os.path.exists(filename):
            color_print(f"El archivo '{filename}' ya no está: termino.", "morado")
            existe_arch = False

if __name__ == '__main__':
    print(active_count())
    x = []
    hebras = []
    num_max = 10
    print("Dame ordenes. Al acabar porn 'FIN'")
    orden = input()
    while orden != "FIN":
        oH = HebraOrdenes(x, orden)
        hebras.append(oH)
        if active_count() < num_max:
            oH.start()
            orden = input()
        else:
            orden = "FIN"
            print("Demasiadas hebras activas, no se aceptan nuevas ordenes.")

        
    print(f"La hebra principal la lista es: {x}")
        