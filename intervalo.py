class Intervalo:
    # Esta clase representa el intervalo de tiempo que maneja un temporizador,
    # con la capacidad de incrementar, decrementar y acabar.
    # Está pensada para ser utilizada en un temporizador.
    def __init__(self, valor: float = 1.0) -> None:
        self.__valor = valor
        self.__acabado = False
        self.__max_permitido = 3.0
        self.__min_permitido = 0.2
        self.__salto = 0.2

    def acabar(self) -> None:
        self.__acabado = True

    def ha_acabado(self) -> bool:
        return self.__acabado

    def incrementa(self) -> None:
        self.__valor = min(self.__max_permitido, self.__valor + self.__salto)

    def decrementa(self) -> None:
        self.__valor = max(self.__min_permitido, self.__valor - self.__salto)

    def valor_actual(self) -> float:
        return self.__valor
