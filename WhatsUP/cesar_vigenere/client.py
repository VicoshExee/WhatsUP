import socket
import threading
from chiffrement_cesar_vigenere import *
from interface import ChatInterface

IP = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choisissez un pseudo : ")
client.send(bytes(encrypt(pseudo), "utf-8"))

# Fonction d'envoi de message
def send_message(message):
    if message:
        client.send(bytes(encrypt(message), "utf-8"))
        interface.clear_entry()
        if message.lower() == "exit":
            client.close()
            interface.root.quit()

# Fonction de réception des messages
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            message = decrypt(message)
            interface.display_message(message)
        except:
            break

# Initialisation de l'interface graphique
interface = ChatInterface(send_message)
interface.update_pseudo(pseudo)

# Thread pour recevoir les messages
thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()

# Lancer l'interface
interface.run()
