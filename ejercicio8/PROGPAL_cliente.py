# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:11:43 2026

@author: usu423
"""

from socket import socket

sckt = socket()
srvr_ip = "localhost"
srvr_puerto = 12345
sckt.connect((srvr_ip, srvr_puerto))

print("Se ha establecido conexión con el servidor. Introduzca el tipo de servicio que desea y posteriormente el mensaje sobre el que ejecutarlo. Presione un \"enter\" vacio dos veces para acabar. ")
tipo = input("TIPO:  ")
peticion = input("MENSAJE:  ")
while peticion and tipo:
    tipo_env = tipo.encode()
    msj_env = peticion.encode()
    sckt.send(tipo_env)
    sckt.send(msj_env)

    msj_rec = sckt.recv(1024)
    respuesta = msj_rec.decode()
    print(f"Según el servidor, '{peticion}' tras '{tipo}' es '{respuesta}'.")
    tipo = input("TIPO:  ")
    peticion = input("MENSAJE:  ")
         
sckt.close()

  