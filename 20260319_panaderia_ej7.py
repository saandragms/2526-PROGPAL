# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 09:03:11 2026

@author: usu424
"""
from threading import Thread


class Panaderia():
    def __init__(self, num_procesos):
        self.num_proc = num_procesos
        self.cogiendoNumero = [False]*self.num_proc
        self.numero = [0]*self.num_proc
        
    def protocolo(self, i : int):
        self.cogiendoNumero[i] = True
        self.numero[i] = 1 + max(self.numero)
        self.cogiendoNumero[i] = False
        for j in range(0,self.num_proc):
            if i !=j:
                while self.cogiendoNumero[j]:
                    pass
                while (self.numero[j]!=0) and (self.numero[j] < self.numero[i] or (self.numero[j] == self.numero[i] and j < i)):
                    pass
        
            
    def postprotocolo(self, i : int):
        self.numero[i] = 0
        
        
class ContadorSeguro():
    def __init__(self, num_procesos: int, inicial: int) -> None:
        self.num_proc = num_procesos
        self.contador = inicial
        self.pan = Panaderia(self.num_proc)
        

    def incrementar(self, i :int) -> None:
        self.pan.protocolo(i)
        self.contador += 1
        self.pan.postprotocolo(i)

    def decrementar(self, i :int) -> None:
        self.pan.protocolo(i)
        self.contador -= 1
        self.pan.postprotocolo(i)

    def valor(self) -> int:
        return self.contador
    
    
class Hebra(Thread):
    def __init__(self, id_hilo: int, contador_compartido: ContadorSeguro):
        super().__init__()
        self.i = id_hilo
        self.contador = contador_compartido 
        
    def run(self):
        for _ in range(100):
            self.contador.incrementar(self.i)
        
        
if __name__ == "__main__":
    
    num_procesos = 50
    inicial = 0
    contador = ContadorSeguro(num_procesos, inicial)
    
    hebras = [Hebra(i, contador) for i in range(0,num_procesos)]
    
    for h in hebras:
        h.start()
        
    for h in hebras:
        h.join()
        
    print("Todos los hilos han terminado.")
    print(f"Valor esperado: {num_procesos * 100}")
    print(f"Valor real del contador: {contador.valor()}")