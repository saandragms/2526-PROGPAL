# -*- coding: utf-8 -*-
"""
Created on Thu Jan 22 09:09:25 2026

@author: sguemes@ucm.es

PROGAMACION PARALELA EJ 1
"""
from itertools import starmap

from multiprocessing import Pool

from typing import Callable

import time

from math import sin,pi

def suma1(x: int) -> int:
    return x + 1

def suma(x: int, y: int) -> int:
    return x + y

def area_rect(una_funcion: Callable[[float], float],
              inf: float, sup: float) -> float:
    return (sup - inf) * una_funcion((inf + sup) / 2)

def integral_sec(la_funcion: Callable[[float], float],
                 inf: float, sup: float,
                 cant_interv: int) -> float:
    tareas = [(la_funcion,
               inf + i * (sup - inf) / cant_interv,
               inf + (i + 1) * (sup - inf) / cant_interv)
              for i in range(cant_interv)]
    resultados = starmap(area_rect, tareas)
    return sum(resultados)

def integral_paral_0(una_funcion: Callable[[float], float],
                     inf: float, sup: float,
                     cant_interv: int, cant_proc: int = None) -> float:
    tareas = [(una_funcion,
               inf + i * (sup - inf) / cant_interv,
    inf + (i + 1) * (sup - inf) / cant_interv)
              for i in range(cant_interv)]
    
    # crea un pool de procesos y ponlos a trabajar
    pool = Pool(cant_proc)
    resultados = pool.starmap(area_rect, tareas)
    
    return sum(resultados)

def integral_paral(una_funcion: Callable[[float], float],
                   inf: float, sup: float,
                   cant_interv: int, cant_tareas: int,
                   cant_proc: int = None) -> float:
    tareas = [(una_funcion,
               inf + i * (sup - inf) / cant_tareas,
               inf + (i + 1) * (sup - inf) / cant_tareas, int(cant_interv/cant_tareas))
              for i in range(cant_tareas)]
    
    pool = Pool(cant_proc)
    resultados = pool.starmap(integral_sec, tareas)
    return sum(resultados)



# Para las pruebas.
if __name__ == "__main__":
    
    print("TEST 1 CON 4 INTERVALOS.\n")
    
    n = 4
    
    t00 = time.perf_counter()
    result1 = integral_sec(sin, 0, pi, 4)
    t01 = time.perf_counter()
    print("Resultado del caso 1: ")
    print(result1)
    print("En tiempo: ")
    print(t01 - t00)
    
    t10 = time.perf_counter()
    result2 = integral_paral_0(sin, 0, pi,4, n)
    t11 = time.perf_counter()
    print("Resultado del caso 2: ")
    print(result2)
    print("En tiempo: ")
    print(t11 - t10)
    
    print("\nTEST 2 CON DIFERENTES INTERVALOS.\n")
    for cant_int in [1,10,100,1000]:
        n = cant_int
        print("\nNUMERO DE INTERVALOS:")
        print(n)
        t00 = time.perf_counter()
        result1 = integral_sec(sin, 0, pi, n)
        t01 = time.perf_counter()
        print("Resultado del caso 1: ")
        print(result1)
        print("En tiempo: ")
        print(t01 - t00)
        
        t10 = time.perf_counter()
        result2 = integral_paral_0(sin, 0, pi, n)
        t11 = time.perf_counter()
        print("\nResultado del caso 2: ")
        print(result2)
        print("En tiempo: ")
        print(t11 - t10)
        
        if (n == 1000):
            t20 = time.perf_counter()
            result3 = integral_paral(sin, 0, pi, n, 50)
            t21 = time.perf_counter()
            print("\nResultado del caso 3: ")
            print(result3)
            print("En tiempo: ")
            print(t21 - t20)
    
    

    
    