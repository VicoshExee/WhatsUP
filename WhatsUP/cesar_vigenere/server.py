import socket
import threading
from chiffrement_cesar_vigenere import *

IP = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

clients = []
pseudos = []

def broadcast(message):
    for client in clients:
        client.send(bytes(encrypt(message), "utf-8"))

def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {str(address)}")

        pseudo = client.recv(1024).decode("utf-8")
        pseudo = decrypt(pseudo)

        clients.append(client)
        pseudos.append(pseudo)

        print(f"{pseudo} a rejoint le chat !")
        client.send(bytes(encrypt("Bienvenue sur le chat ! \n"), "utf-8"))
        broadcast(f"{pseudo} a rejoint le chat !")

        thread = threading.Thread(target=handle_client, args=(client, pseudo))
        thread.start()

def handle_client(client, pseudo):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            message = decrypt(message)

            if message == "exit":
                remove_client(client, pseudo)
                break
            else:
                broadcast(f"{pseudo}: {message}")
        except:
            remove_client(client, pseudo)
            break

def remove_client(client, pseudo):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        pseudos.pop(index)
        client.close()
        broadcast(f"{pseudo} a quitté le chat !")

print("Le serveur est en marche !")
handle_connexion()
