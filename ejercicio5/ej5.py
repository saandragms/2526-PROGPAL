# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 09:20:04 2026

@author: saand
"""
from multiprocessing import Process, Queue

import cv2
def detecta_bordes(nombre_del_original: str,
                   nombre_para_el_resultado: str) -> None:
    imagen = cv2.imread(nombre_del_original)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    bordes = cv2.Canny(blur, 100, 200)
    cv2.imwrite(nombre_para_el_resultado, bordes)
    
class Proc1(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
    def run(self):
        nombre_im = self.q_in.get()
        while nombre_im is not None:
            imagen = cv2.imread(nombre_im)
            self.q_out.put(imagen)
            nombre_im = self.q_in.get()
        self.q_out.put(None)
        
class Proc2(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
    def run(self):
        imagen = self.q_in.get()
        while imagen is not None:
            gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            self.q_out.put(gris)
            imagen = self.q_in.get()
        self.q_out.put(None)

class Proc3(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
    def run(self):
        gris = self.q_in.get()
        while gris is not None:
            blur = cv2.GaussianBlur(gris, (5, 5), 0)
            self.q_out.put(blur)
            gris = self.q_in.get()
        self.q_out.put(None)

class Proc4(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
    def run(self):
        blur = self.q_in.get()
        while blur is not None:
            bordes = cv2.Canny(blur, 100, 200)
            self.q_out.put(bordes)
            blur = self.q_in.get()
        self.q_out.put(None)

class Proc5(Process):
    def __init__(self, nombre_out: str, q_in: Queue):
        super().__init__()
        self.nombre = nombre_out
        self.q_in = q_in
        
    def run(self):
        bordes = self.q_in.get()
        i = 0
        while bordes is not None:
            cv2.imwrite(self.nombre + f"{i}.png", bordes)
            bordes = self.q_in.get()
            i +=1
            
if __name__ == "__main__":
    imagenes = ["Bot_Pic_IA.png", "Maritimo.png", "Villareal.png", "Ciclo.png", "ForceSupport.jpg" ]
        
    # 1. Crear las colas que conectarán los procesos
    q0 = Queue() # Para pasar nombres a Proc1
    q1 = Queue() # Proc1 -> Proc2
    q2 = Queue() # Proc2 -> Proc3
    q3 = Queue() # Proc3 -> Proc4
    q4 = Queue() # Proc4 -> Proc5
        
    # 2. Instanciar los procesos conectándolos con las colas
    p1 = Proc1(q0, q1)
    p2 = Proc2(q1, q2)
    p3 = Proc3(q2, q3)
    p4 = Proc4(q3, q4)
    p5 = Proc5("res_", q4)
    
    procesos = [p1, p2, p3, p4, p5]

    # 3. Arrancar los procesos (se quedarán esperando en el primer .get())
    for p in procesos:
        p.start()
        
    # 4. Alimentar la primera cola con los nombres de los archivos
    for imagen in imagenes:
        q0.put(imagen)
    q0.put(None)
    
    # 5. Esperar a que todos los procesos terminen ordenadamente
    for p in procesos:
        p.join()
        
    print("¡Procesamiento en pipeline completado!")
