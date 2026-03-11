import socket
import threading

def recibir_mensajes(mi_socket):
    while True:
        try:
            mensaje = mi_socket.recv(1024).decode('utf-8')
            if not mensaje:
                break
            print(f"\n[SERVIDOR DICE]: {mensaje}")
            print("Tú: ", end="")
        except:
            break

IP_DESTINO = '192.168.107.95' 
PORT_DESTINO = 65432

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((IP_DESTINO, PORT_DESTINO))
    print("[+] ¡Conexión exitosa al servidor!")
except:
    print("[!] No se pudo conectar. ¿El servidor está prendido?")
    exit()

hilo_escucha = threading.Thread(target=recibir_mensajes, args=(cliente,))
hilo_escucha.daemon = True
hilo_escucha.start()

while True:
    mi_mensaje = input("Tú: ")
    cliente.send(mi_mensaje.encode('utf-8'))
    
    if mi_mensaje.lower() == 'terminar':
        break

cliente.close()