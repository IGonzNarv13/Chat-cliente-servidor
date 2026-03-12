import socket
import threading

clientes = {}
historial_mensajes = []

def broadcast(mensaje, conexion_remitente):
    nombre = clientes[conexion_remitente]
    formato_mensaje = f"[{nombre}]: {mensaje.decode('utf-8')}"
    print(formato_mensaje)
    historial_mensajes.append(formato_mensaje)
    
    for cliente in clientes:
        if cliente != conexion_remitente:
            try:
                cliente.send(formato_mensaje.encode('utf-8'))
            except:
                remover(cliente)

def manejar_cliente(conn, addr):
    try:
        nickname = conn.recv(1024).decode('utf-8')
        clientes[conn] = nickname
        print(f"[+] {nickname} ({addr}) se ha unido al chat.")

        if historial_mensajes:
            conn.send("*** HISTORIAL DE MENSAJES ***\n".encode('utf-8'))
            for msg_pasado in historial_mensajes:
                conn.send((msg_pasado + "\n").encode('utf-8'))
            conn.send("****************************\n".encode('utf-8'))

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
        conn.close()

HOST = '0.0.0.0'
PORT = 65432

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()

print(f"Servidor de chat iniciado en el puerto {PORT}...")

while True:
    conn, addr = servidor.accept()
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.start()