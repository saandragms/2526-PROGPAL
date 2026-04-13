from time import sleep
from threading import Thread
from intervalo import Intervalo


class PintaBarra(Thread):
    def __init__(self, intervalo: Intervalo) -> None:
        super().__init__()
        self.__intervalo = intervalo

    def run(self) -> None:
        while not self.__intervalo.ha_acabado():
            sleep(self.__intervalo.valor_actual())
            print("█", end="")
