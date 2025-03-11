import socket
import threading
import rsa
from chiffrement import encrypt_message
from echange import cle_generate, echange_secret
from interface import ChatInterface

IP = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Récupération cle RSA
public_key_data = client.recv(1024)
public_key = rsa.PublicKey.load_pkcs1(public_key_data)

pseudo = input("Choisissez un pseudo : ")
client.send(bytes(pseudo, "utf-8"))

# echange cle ciffie-hellman
dh_params = client.recv(1024).decode().split(',')
prime, base, server_public_dh = int(dh_params[0]), int(dh_params[1]), int(dh_params[2])
_, _, client_private_dh, client_public_dh = cle_generate()
client.send(str(client_public_dh).encode())
shared_secret = echange_secret(client_private_dh, server_public_dh, prime)
print(f"clé diffie-hellman {shared_secret}")

def send_message(message):
    if message:
        encrypted_message = encrypt_message(message, public_key)
        client.send(encrypted_message)
        interface.clear_entry()
        if message.lower() == "exit123":
            client.close()

def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            interface.display_message(message)
        except:
            break

interface = ChatInterface(send_message)
interface.update_pseudo(pseudo)

thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()

interface.run()
