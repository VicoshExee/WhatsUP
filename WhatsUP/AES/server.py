import socket
import threading
from aes_diffie_hellman import generate_keys, shared_key, encrypt_message, decrypt_message

IP = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

clients = []
pseudos = []
shared_secrets = {}

# Diffusion des messages à tous les clients
def broadcast(message, exclude_client=None):
    for client in clients:
        if client != exclude_client:
            shared_secret = shared_secrets.get(client)
            if shared_secret:
                client.send(encrypt_message(message, shared_secret).encode("utf-8"))

# Gestion des connexions
def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {str(address)}")

        # Échange de clés Diffie-Hellman
        p, g, private_key, public_key = generate_keys()
        client_public_key = int(client.recv(1024).decode("utf-8"))
        client.send(str(public_key).encode("utf-8"))

        shared_secret = shared_key(client_public_key, private_key, p)
        shared_secrets[client] = shared_secret

        pseudo = decrypt_message(client.recv(1024).decode("utf-8"), shared_secret)
        clients.append(client)
        pseudos.append(pseudo)

        print(f"{pseudo} a rejoint le chat !")
        client.send(encrypt_message("Bienvenue sur le chat !", shared_secret).encode("utf-8"))
        broadcast(f"{pseudo} a rejoint le chat !", exclude_client=client)

        thread = threading.Thread(target=handle_client, args=(client, pseudo))
        thread.start()

# Gestion des clients
def handle_client(client, pseudo):
    while True:
        try:
            shared_secret = shared_secrets.get(client)
            if not shared_secret:
                continue

            message = decrypt_message(client.recv(1024).decode("utf-8"), shared_secret)
            if message == "exit":
                remove_client(client, pseudo)
                break
            else:
                broadcast(f"{pseudo}: {message}", exclude_client=client)
        except Exception as e:
            print(f"Erreur client : {e}")
            remove_client(client, pseudo)
            break

# Suppression du client
def remove_client(client, pseudo):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        pseudos.pop(index)
        shared_secrets.pop(client, None)
        client.close()
        broadcast(f"{pseudo} a quitté le chat !")

print("Le serveur est en marche !")
handle_connexion()
