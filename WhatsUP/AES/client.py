import socket
import threading
from aes_diffie_hellman import generate_keys, shared_key, encrypt_message, decrypt_message
from interface import ChatInterface

IP = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Génération des clés Diffie-Hellman
p, g, private_key, public_key = generate_keys()
client.send(str(public_key).encode("utf-8"))

# Réception de la clé publique du serveur
server_public_key = int(client.recv(1024).decode("utf-8"))
shared_key = shared_key(server_public_key, private_key, p)

pseudo = input("Choisissez un pseudo : ")
client.send(encrypt_message(pseudo, shared_key).encode("utf-8"))

# Fonction d'envoi de message
def send_message(message):
    if message:
        client.send(encrypt_message(message, shared_key).encode("utf-8"))
        interface.clear_entry()
        if message.lower() == "exit":
            client.close()
            interface.root.quit()

# Fonction de réception des messages
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            message = decrypt_message(message, shared_key)
            interface.display_message(message)
        except Exception as e:
            print(f"Erreur de réception : {e}")
            break

interface = ChatInterface(send_message)
interface.update_pseudo(pseudo)

thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()
interface.run()