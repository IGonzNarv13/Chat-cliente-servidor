import socket
import threading

def recibir_mensajes(s):
    while True:
        try:
            data = s.recv(1024)
            if not data: break
            print(f"\n{data.decode('utf-8')}\nTú: ", end="")
        except:
            break

IP_SERVIDOR = '192.168.107.95'
PORT = 65432

nickname = input("Ingresa tu nickname: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((IP_SERVIDOR, PORT))
    s.send(nickname.encode('utf-8'))
    print(f"Conectado como {nickname}. Escribe 'salir' para finalizar.")

    threading.Thread(target=recibir_mensajes, args=(s,), daemon=True).start()

    while True:
        msg = input("Tú: ")
        if msg.lower() == 'salir': break
        s.send(msg.encode('utf-8'))
finally:
    s.close()