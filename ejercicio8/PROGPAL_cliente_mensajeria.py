from socket import socket

sckt = socket()
srvr_ip = "localhost"
srvr_puerto = 12345
sckt.connect((srvr_ip, srvr_puerto))

nombre_cliente = input("Introduzca su nombre de usuario: ")
sckt.send(nombre_cliente.encode())

print(
    "Se ha establecido conexión con el servidor. Introduzca los mensajes a enviar. Presione un \"enter\" cuando haya acabado. ")
peticion = input("MENSAJE:  ")
while peticion:
    msj_env = peticion.encode()
    sckt.send(msj_env)

    peticion = input("MENSAJE:  ")

acceder_mensajes = input("¿Desea leer los mensajes pendientes? [Y/N]: ")

if acceder_mensajes=="Y":
    sckt.send("LEER".encode())
    mensajes_recibidos = sckt.recv(1024)
    print("El servidor indica que tiene los siguientes mensajes sin leer: ")
    print(mensajes_recibidos.decode())

sckt.close()

