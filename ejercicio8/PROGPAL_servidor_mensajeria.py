from threading import  Thread, Lock
from socket import socket

class Almacen():
    def __init__(self):
        self.lista_mensajes = []
        self.lock = Lock()

    def add_mensaje(self, msj):
        with self.lock:
            self.lista_mensajes.append(msj)

    def mostrar_mensajes(self):
        with self.lock:
            return list(self.lista_mensajes)



class AtiendeCliente(Thread):
    def __init__(self, almacen, cl_socket, contador_clientes):
        super().__init__()
        self.alm = almacen
        self.cl_socket = cl_socket
        self.id_cliente = contador_clientes

    def run(self):
        try:
            nombre_cliente = self.cl_socket.recv(1024).decode()
            while True:
                msj_rec = self.cl_socket.recv(1024)
                if not msj_rec:  # Si el cliente cierra la conexión
                    break
                orden = msj_rec.decode()
                if orden == "LEER":
                    chat = self.alm.mostrar_mensajes()
                    chat_txt = "\n".join(chat)
                    chat_env = chat_txt.encode()
                    self.cl_socket.send(chat_env)

                else:
                    mensaje = f"{nombre_cliente}: {orden}"
                    self.alm.add_mensaje(mensaje)
                    print(f"Mensaje guardado de {nombre_cliente}")


        except Exception as e:
            print(f"Error: {e}")

        finally:
            self.cl_socket.close()
            print(f"Conexión con cliente #{self.id_cliente} cerrada.")




# --- Configuración principal ---
if __name__ == "__main__":
    almacen = Almacen()

    srvr_socket = socket()
    ip_addr = "localhost"
    puerto = 12345

    srvr_socket.bind((ip_addr, puerto))
    srvr_socket.listen()

    print(f"Servidor escuchando en {ip_addr}:{puerto}...")
    contador_clientes = 0

    while True:
        cl_socket, _ = srvr_socket.accept()
        contador_clientes += 1
        cl_thread = AtiendeCliente(almacen, cl_socket, contador_clientes)
        cl_thread.start()

    # srvr_socket.close()
