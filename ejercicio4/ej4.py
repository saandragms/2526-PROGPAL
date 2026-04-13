# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 09:11:41 2026

@author: saand
"""
from multiprocessing import Process, Queue
import time

def lucas_lehmer(p: int) -> bool:
    if p == 2:
        return True
    m = 2**p - 1
    s = 4
    for _ in range(p - 2):
        s = (s * s - 2) % m
    return s == 0

""" 
VERSION 1
"""
class PVer1(Process):
    def __init__(self, q: Queue):
        super().__init__()
        self.cola_tareas = q
        
    def run(self):
        p = self.cola_tareas.get()
        while p is not None:
            es_primo = lucas_lehmer(p)
            if es_primo:
                # Usamos self.name para ver qué proceso exacto ha encontrado el primo
                print(f"[+] {self.name}: ¡ÉXITO! 2^{p}-1 ES un primo de Mersenne.")
            else:
                print(f"[-] {self.name}: 2^{p}-1 NO es primo.")
            p = self.cola_tareas.get()
                      
                      
if __name__ == "__main__":
    
    t0 = time.perf_counter()
    cola_tareas = Queue()
    
    primos_a_probar = [521, 607, 1279, 2203, 2281, 3217, 4423, 9689, 9941]
    
    # Llenamos la cola
    for primo in primos_a_probar:
        cola_tareas.put(primo)
        
    num_proc = 4
    for _ in range(num_proc):
        cola_tareas.put(None)
        
    procesos = []
    
    # Creamos e iniciamos las instancias de tu clase Trabajador
    for _ in range(num_proc):
        # Instanciamos la clase pasándole la cola
        p = PVer1(cola_tareas) 
        procesos.append(p)
        # Al llamar a start(), Python invoca por debajo el método run() de la clase
        p.start()
        
    for p in procesos:
        p.join()
    t1 = time.perf_counter()
        
    print("\n--- Primera versión finalizada en : ")
    print(f'{t1 - t0:.4f} segundos.---\n')

""" 
VERSION 2
"""
class PVer2(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
        
    def run(self):
        p = self.q_in.get()
        while p is not None:
            es_primo = lucas_lehmer(p)
            self.q_out.put((p,es_primo))
            p = self.q_in.get()
                      
                      
if __name__ == "__main__":
    
    t0 = time.perf_counter()
    
    cola_tareas_in = Queue()
    cola_tareas_out = Queue()
    
    primos_a_probar = [521, 607, 1279, 2203, 2281, 3217, 4423, 9689, 9941]
    
    # Llenamos la cola
    for primo in primos_a_probar:
        cola_tareas_in.put(primo)
        
    num_proc = 4
    for _ in range(num_proc):
        cola_tareas_in.put(None)
        
    procesos = []
    
    # Creamos e iniciamos las instancias de tu clase Trabajador
    for _ in range(num_proc):
        # Instanciamos la clase pasándole la cola
        p = PVer2(cola_tareas_in, cola_tareas_out) 
        procesos.append(p)
        # Al llamar a start(), Python invoca por debajo el método run() de la clase
        p.start()
        
    for p in procesos:
        p.join()
        
    # Mientras la cola de resultados no esté vacía...
    while not cola_tareas_out.empty():
        # Sacamos la tupla que metió el trabajador
        p, es_primo = cola_tareas_out.get() 
        
        if es_primo:
            print(f"[+] PVer2: ¡ÉXITO! 2^{p}-1 ES un primo de Mersenne.")
        else:
            print(f"[-] PVer2: 2^{p}-1 NO es primo.")
            
    t1 = time.perf_counter()
        
    print("\n--- Segunda versión finalizada en : ")
    print(f'{t1 - t0:.4f} segundos.---\n')

"""
VERSION 3
"""
class PVer3(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
        
    def run(self):
        p = self.q_in.get()
        while p is not None:
            es_primo = lucas_lehmer(p)
            self.q_out.put((p,es_primo))
            p = self.q_in.get()
        self.q_out.put(None)
                      
                      
if __name__ == "__main__":
    
    t0 = time.perf_counter()
    
    cola_tareas_in = Queue()
    cola_tareas_out = Queue()
    
    primos_a_probar = [521, 607, 1279, 2203, 2281, 3217, 4423, 9689, 9941]
    
    # Llenamos la cola
    for primo in primos_a_probar:
        cola_tareas_in.put(primo)
        
    num_proc = 4
    for _ in range(num_proc):
        cola_tareas_in.put(None)
        
    procesos = []
    
    # Creamos e iniciamos las instancias de tu clase Trabajador
    for _ in range(num_proc):
        # Instanciamos la clase pasándole la cola
        p = PVer3(cola_tareas_in, cola_tareas_out) 
        procesos.append(p)
        # Al llamar a start(), Python invoca por debajo el método run() de la clase
        p.start()
    
    trabajadores_terminados = 0

    while trabajadores_terminados < num_proc:
        sol = cola_tareas_out.get()
        if sol is None:
            trabajadores_terminados +=1
        else:
            if sol[1]:
                print(f"[+] PVer3: ¡ÉXITO! 2^{sol[0]}-1 ES un primo de Mersenne.")
            else:
                print(f"[-] PVer3: 2^{sol[0]}-1 NO es primo.")
        
        
    for p in procesos:
        p.join()
        
    t1 = time.perf_counter()
    
    print("\n--- Tercera versión finalizada en : ")
    print(f'{t1 - t0:.4f} segundos.---\n')
        
"""
VERSION  4
"""

class PVer4(Process):
    def __init__(self, q_in: Queue, q_out: Queue):
        super().__init__()
        self.q_in = q_in
        self.q_out = q_out
        
        
    def run(self):
        p = self.q_in.get()
        while p is not None:
            es_primo = lucas_lehmer(p)
            self.q_out.put((p,es_primo))
            p = self.q_in.get()
        self.q_out.put(None)
        
class Generador(Process):
    def __init__(self, q_out: Queue, num_workers: int, limite_superior: int = 10000):
        super().__init__()
        self.q_out = q_out
        self.num_workers = num_workers
        self.limite = limite_superior

    def es_primo_basico(self, n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    def run(self):
        # Empezamos desde el primer primo de Mersenne [cite: 33]
        n = 2
        while n < self.limite:
            if self.es_primo_basico(n):
                # Ponemos el primo en la cola para que un worker lo use como exponente 
                self.q_out.put(n)
            n += 1
        
        # Al llegar al límite, enviamos la señal de parada a cada worker [cite: 12]
        for _ in range(self.num_workers):
            self.q_out.put(None)

                      
                      
if __name__ == "__main__":
    
    t0 = time.perf_counter()
    
    cola_tareas_in = Queue()
    cola_tareas_out = Queue()

    num_proc = 4
    limite_exponentes = 1000  # Puedes subirlo a 10000 según el PDF
    
    generador = Generador(cola_tareas_in, num_proc, limite_exponentes)
    generador.start()
    
    procesos = []
    
    for _ in range(num_proc):
        # Instanciamos la clase pasándole la cola
        p = PVer4(cola_tareas_in, cola_tareas_out) 
        procesos.append(p)
        p.start()
        
    trabajadores_terminados = 0

    while trabajadores_terminados < num_proc:
        sol = cola_tareas_out.get()
        if sol is None:
            trabajadores_terminados +=1
        else:
            if sol[1]:
                print(f"[+] PVer4: ¡ÉXITO! 2^{sol[0]}-1 ES un primo de Mersenne.")
            else:
                print(f"[-] PVer4: 2^{sol[0]}-1 NO es primo.")
        
        
    for p in procesos:
        p.join()
        
    generador.join()
    
    t1 = time.perf_counter()
        
    print("\n--- Cuarta versión finalizada en : ")
    print(f'{t1 - t0:.4f} segundos.---\n')
        
