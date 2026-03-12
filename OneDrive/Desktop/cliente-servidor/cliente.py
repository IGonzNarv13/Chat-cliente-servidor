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

IP_UBUNTU = '192.168.100.44'
PORT = 65432

nick = input("Ingresa tu nickname para el chat: ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((IP_UBUNTU, PORT))
    s.send(nick.encode('utf-8'))
    print(f"[!] Conectado como {nick}. Escribe 'salir' para abandonar.")
    
    threading.Thread(target=recibir_mensajes, args=(s,), daemon=True).start()

    while True:
        msg = input("Tú: ")
        if msg.lower() == 'salir': break
        s.send(msg.encode('utf-8'))
except Exception as e:
    print(f"[!] Error de conexión: {e}")
finally:
    s.close()