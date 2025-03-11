import socket
import threading
from chiffrement import generate_keys, decrypt_message
from echange import cle_generate, echange_secret

IP = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

clients = []
pseudos = []


public_key, private_key = generate_keys()

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {str(address)}")
        
        client.send(public_key.save_pkcs1())  # envoie cle RSA
        pseudo = client.recv(1024).decode("utf-8")
        
        # echange cle ciffie-hellman
        prime, base, server_private_dh, server_public_dh = cle_generate()
        client.send(f"{prime},{base},{server_public_dh}".encode())
        client_public_dh = int(client.recv(1024).decode())
        shared_secret = echange_secret(server_private_dh, client_public_dh, prime)
        
        clients.append(client)
        pseudos.append(pseudo)
        print(f"{pseudo} a rejoint le chat !")
        broadcast(f"{pseudo} a rejoint le chat !".encode())
        
        thread = threading.Thread(target=handle_client, args=(client, pseudo))
        thread.start()

def handle_client(client, pseudo):
    while True:
        try:
            encrypted_message = client.recv(1024)
            message = decrypt_message(encrypted_message, private_key)
            if message == "exit123":
                remove_client(client, pseudo)
                break
            else:
                broadcast(f"{pseudo}: {message}".encode())
        except:
            remove_client(client, pseudo)
            break

def remove_client(client, pseudo):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        pseudos.pop(index)
        client.close()
        broadcast(f"{pseudo} a quitté le chat !".encode())

print("Le serveur est en marche !")
handle_connexion()
