import socket
import threading

# Diccionario para asociar conexiones con nicknames {conexion: nickname}
clientes = {}

def broadcast(mensaje, conexion_remitente):
    """Reenvía el mensaje a todos con el nombre del remitente"""
    nombre = clientes[conexion_remitente]
    formato_mensaje = f"[{nombre}]: {mensaje.decode('utf-8')}"
    
    for cliente in clientes:
        if cliente != conexion_remitente:
            try:
                cliente.send(formato_mensaje.encode('utf-8'))
            except:
                remover(cliente)

def manejar_cliente(conn, addr):
    try:
        # El primer mensaje que recibimos de este cliente es su Nickname
        nickname = conn.recv(1024).decode('utf-8')
        clientes[conn] = nickname
        print(f"[+] {nickname} ({addr}) se ha unido al chat.")
        
        # Avisar a los demás que alguien entró
        aviso = f"*** {nickname} ha entrado al chat ***".encode('utf-8')
        for c in clientes:
            if c != conn: c.send(aviso)

        while True:
            mensaje = conn.recv(1024)
            if mensaje:
                broadcast(mensaje, conn)
            else:
                remover(conn)
                break
    except:
        remover(conn)

def remover(conn):
    if conn in clientes:
        nombre = clientes[conn]
        print(f"[-] {nombre} se ha desconectado.")
        del clientes[conn]

HOST = '0.0.0.0'
PORT = 65432
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen(5) # Capacidad de la sala de espera

print(f"[*] Servidor de chat grupal activo en el puerto {PORT}...")

while True:
    conn, addr = servidor.accept()
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.start()