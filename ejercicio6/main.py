from pinta import PintaBarra
from intervalo import Intervalo
from interaccion import Interaccion


intervalo = Intervalo(valor=1.0)
h_interaccion = Interaccion(intervalo)
h_pinta = PintaBarra(intervalo)
h_interaccion.start()
h_pinta.start()
h_interaccion.join()
h_pinta.join()
print("programa terminado")
