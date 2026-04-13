# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:14:07 2026

@author: usu423
"""
from threading import  Thread
from socket import socket

class AtiendeCliente(Thread):

    def __init__(self, cl_socket, contador_clientes):
        super().__init__()
        self.cl_socket = cl_socket
        self.id_cliente = contador_clientes

    def run(self):
        try:
            tipo_rec = self.cl_socket.recv(1024)
            while tipo_rec:
                msj_rec = self.cl_socket.recv(1024)
                if not msj_rec:
                    break

                tipo = tipo_rec.decode().upper()
                peticion = msj_rec.decode()

                if tipo == "MAYUS":
                    respuesta = peticion.upper()
                elif tipo == "MINUS":
                    respuesta = peticion.lower()
                else:
                    respuesta = "ERROR: Tipo de servicio solicitado no válido"

                msj_env = respuesta.encode()
                self.cl_socket.send(msj_env)

                tipo_rec = self.cl_socket.recv(1024)

        except Exception as e:
            print(f"Error atendiendo al cliente: {e}")

        finally:
            self.cl_socket.close()
            print(f"Conexión con cliente #{self.id_cliente} cerrada.")




# --- Configuración principal ---
if __name__ == "__main__":
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
        cl_thread = AtiendeCliente(cl_socket, contador_clientes)
        cl_thread.start()

    # srvr_socket.close()
