import socket
import threading
import random
import configparser
import os


"""
--- READ ME---
THIS SERVER WAS DEVELOPED IN 2021 BY JACOB CORNELISON OF JAKE SYSTEMS (jakesystems.us)
DEVELOPED WITH PYTHON 3.9.2 64-BIT
FEEL FREE TO MODIFY THE SERVER TO MEET YOUR OWN NEEDS

JACOB CORNELISON NOT RESPONSIBLE FOR DAMAGE CAUSED BY PROPER OR IMPROPER USE OF THIS SOFTWARE, NOR AM I RESPONSIBLE FOR ILLEGAL ACTIONS PERFORMED IN INCORPORATION WITH THIS SOFTWARE
"""

#default port should be 9090 and server should be 127.0.0.1

name = input("Enter a server nickname")
host = input("Internal IP?")
port = input("Server port?")
HOST = host
PORT = int(port)
NAME = name

version = "1.0.0 ALPHA"

if name == None:
    NAME = "default name"

if host == None:
    HOST = "127.0.0.1"

if port == None:
    PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

#welcomes = [f"{nickname} joined the chat\n", f"{nickname} connected to the server\n"]



#broadcast function - broadcasts content to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handle function
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove[nickname]

#recieve function - recieves messages from one client and processes
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        client.send("Connected to the server\n".encode("utf-8"))

        for client in clients:
            client.send(f"{nickname} connected to {NAME}\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()




print(f"Server is ready as {NAME}")
print(f"Running at {HOST}:{PORT}")
recieve()


#{nicknames[clients.index(client)]}: 
