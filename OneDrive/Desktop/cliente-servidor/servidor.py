import socket
import threading

def recibir_mensajes(conexion):
    while True:
        try:
            mensaje = conexion.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"\n[CLIENTE DICE]: {mensaje}")
            print("Tú: ", end="")
        except:
            break
    print("\n[!] Conexión terminada.")

HOST = '0.0.0.0'
PORT = 65432 

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"[*] Servidor iniciado en el puerto {PORT}. Esperando al cliente...")
conexion, direccion = servidor.accept()

print(f"[+] ¡Conectado con {direccion}!")

hilo_escucha = threading.Thread(target=recibir_mensajes, args=(conexion,))
hilo_escucha.daemon = True
hilo_escucha.start()

while True:
    mi_mensaje = input("Tú: ")
    conexion.send(mi_mensaje.encode('utf-8'))
    if mi_mensaje.lower() == 'terminar':
        break
conexion.close()