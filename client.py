from tkinter import *
from tkinter import scrolledtext
import socket
import threading

# Paramètres de connexion
IP = "127.0.0.1"
PORT = 55555

# Création du socket client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

# Demande du pseudo
pseudo = input("Choisissez un pseudo : ")
client.send(bytes(pseudo, "utf-8"))

# Création de l'interface graphique
root = Tk()
root.title("Client Chat")
root.geometry("500x400")

# Zone de texte pour afficher les messages
chat_area = scrolledtext.ScrolledText(root, wrap=WORD, state=DISABLED, width=60, height=15)
chat_area.pack(pady=10)

# Champ pour taper le message
message_entry = Entry(root, width=50)
message_entry.pack(pady=5)

# Fonction pour envoyer un message
def send_message():
    message = message_entry.get()
    if message:
        client.send(bytes(message, "utf-8"))
        message_entry.delete(0, END)  # Efface le champ après l'envoi
        if message.lower() == "exit":
            client.close()
            root.quit()

# Bouton pour envoyer le message
send_button = Button(root, text="Envoyer", command=send_message)
send_button.pack(pady=5)

# Fonction pour recevoir les messages
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            chat_area.config(state=NORMAL)  # Activer la modification de la zone de texte
            chat_area.insert(END, message + "\n")
            chat_area.config(state=DISABLED)  # Désactiver la modification après ajout
            chat_area.yview(END)  # Faire défiler vers le bas
        except:
            break

# Thread pour écouter les messages entrants
thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()

# Lancer l'interface graphique
root.mainloop()
