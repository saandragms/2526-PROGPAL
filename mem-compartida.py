from multiprocessing import Process
from threading import Thread


class HebraEj(Thread):
    def __init__(self, lista: list[int], nuevo_elem: int) -> None:
        super().__init__()
        self.nuevo_elem = nuevo_elem
        self.lista = lista

    def run(self) -> None:
        self.lista.append(self.nuevo_elem)
        print(f'en la hebra hija, la lista es {self.lista}')


class ProcesoEj(Process):
    def __init__(self, lista: list[int], nuevo_elem: int) -> None:
        super().__init__()
        self.nuevo_elem = nuevo_elem
        self.lista = lista

    def run(self) -> None:
        self.lista.append(self.nuevo_elem)
        print(f'en el proceso hijo, la lista es {self.lista}')

if __name__ == '__main__':
    x = []
    a33 = HebraEj(x, 33)
    a55 = HebraEj(x, 55)
    a33.start()
    a55.start()
    a33.join()
    a55.join()
    print(f'en la hebra principal, la lista es {x}')
    
    print("--------------------")
    
    x = []
    a33 = ProcesoEj(x, 33)
    a55 = ProcesoEj(x, 55)
    a33.start()
    a55.start()
    a33.join()
    a55.join()
    print(f'en el proceso principal, la lista es {x}')
