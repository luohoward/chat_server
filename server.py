import socket
import select
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("localhost", 9000))

server.listen(100)

clients = []

def clientThread(conn, addr):
    conn.send("Welcome to my chatroom".encode())

    while True:
        try:
            message = conn.recv(2048).decode()
            if message:
                message = addr[0] + ": " + message
                print(clients)
                broadcast(message, conn)

            else:
                remove(conn)
        except:
            continue

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 

while True:
    conn, addr = server.accept()
    
    clients.append(conn)

    print(addr[0] + "connected")
    start_new_thread(clientThread, (conn, addr))

conn.close()
server.close()

