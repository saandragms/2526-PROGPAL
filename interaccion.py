from threading import Thread
from intervalo import Intervalo


class Interaccion(Thread):
    def __init__(self, intervalo: Intervalo) -> None:
        super().__init__()
        self.__intervalo = intervalo

    def run(self) -> None:
        while not self.__intervalo.ha_acabado():
            usu_input = input()
            if usu_input == "+":
                self.__intervalo.incrementa()
            elif usu_input == "-":
                self.__intervalo.decrementa()
            elif usu_input == "q":
                self.__intervalo.acabar()
