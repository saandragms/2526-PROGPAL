# -*- coding: utf-8 -*-
"""
PROGPAL EJ3: FIRE y Montecarlo.

Created on Thu Feb  5 09:12:14 2026

@author: saand
"""
import time
import os
from os import listdir
import random
from multiprocessing import Process

def una_simulacion(capital_inicial: float, esperanza_de_vida: int,
                   gasto_anual: float, mu: float, sigma: float) -> bool:
    capital_actual = capital_inicial
    anyos_restantes = esperanza_de_vida
    while capital_actual > 0 and anyos_restantes > 0:
        variacion_inversion = random.gauss(mu, sigma)
        capital_actual = capital_actual * variacion_inversion - gasto_anual
        anyos_restantes -= 1
    return capital_actual > 0

class Proceso_1(Process):
    def __init__(self, n, capital_ini, esperanza_vida, gasto_anual, mu, sigma, archivo) -> None:
        super().__init__()
        self.num_sim = n
        self.cap_ini = capital_ini
        self.esp_vida = esperanza_de_vida
        self.gasto_anual = gasto_anual
        self.mu = mu
        self.sigma = sigma
        self.nombre_archivo = archivo
        
    def run(self) -> int:
        cantidad_exitos = 0
         
        mu = self.mu
        sigma = self.sigma

        capital_inicial = self.cap_ini
        esperanza_de_vida = self.esp_vida
        gasto_anual = self.gasto_anual
        
        for s in range(self.num_sim):
            cantidad_exitos += una_simulacion(capital_inicial, esperanza_de_vida, gasto_anual,
                                             mu, sigma) 
            
        #print("Cantidad exitos:")
        #print(cantidad_exitos)
        with open(self.nombre_archivo, 'w') as archivo:
            archivo.write(f"{cantidad_exitos},{self.num_sim}")
        
class Resultados(Process):
    def __init__(self, foldername: str, archivo_final: str):
        super().__init__()
        self.foldername = foldername
        self.archivo_final = archivo_final

    def run(self):
        total_exitos = 0
        total_simulaciones = 0
        for filename in listdir(self.foldername):
            if filename.startswith("res_"):
                folderfilename = os.path.join(self.foldername, filename)
                with open(folderfilename, "r") as f:
                    linea = f.read().split(",")
                    total_exitos += int(linea[0])
                    total_simulaciones += int(linea[1])
        probabilidad_exito = total_exitos / total_simulaciones
        with open(self.archivo_final, "w") as f:
            f.write(f"{probabilidad_exito}")


if __name__ == '__main__':
    cant_simulaciones = 100_000
    cant_procesos = 4
    
    mu = 1.06
    sigma = 0.15

    capital_inicial = 35_000
    esperanza_de_vida = 65
    gasto_anual = 1_500
    
    t0 = time.perf_counter()
    print("\nCASO CON PARALELO:")
    
    carpeta = "resultados"
    os.makedirs(carpeta, exist_ok=True)
    cant_simulaciones_por_proceso = cant_simulaciones // cant_procesos
    procesos = []
    
    for nr_proc in range(cant_procesos):
        p = Proceso_1(cant_simulaciones_por_proceso, capital_inicial, esperanza_de_vida,
                      gasto_anual, mu, sigma, f"resultados/res_{nr_proc}.txt")
        procesos.append(p)
        p.start()
        
    for p in procesos:
        p.join()
        
    # crear un nuevo proceso para procesar los resultados. leer cada archivo obviamente pierde efectividad.
    archivo_final = "final"
    resultado_proceso = Resultados(carpeta, archivo_final)
    resultado_proceso.start()
    resultado_proceso.join()
    # lee el resultado del archivo y lo muestra
    with open(archivo_final, "r") as f:
        print("La probabilidad de éxito es:", f.read())
        
    t1 = time.perf_counter()
    print(f'tiempo con paralelo: {t1 - t0:.4f} segundos')
