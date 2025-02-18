from tkinter import *
from tkinter import scrolledtext
import socket
import threading

IP = "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

pseudo = input("Choisissez un pseudo : ")
client.send(bytes(pseudo, "utf-8"))

# Interface graphique
root = Tk()
root.title("WhatsUp")
root.geometry("500x400")

chat_area = scrolledtext.ScrolledText(root, wrap=WORD, state=DISABLED, width=60, height=15)
chat_area.pack(pady=10, padx=10)

pseudo_label = Label(root, text=f"Pseudo : {pseudo}", font=("Arial", 10, "bold"))
pseudo_label.pack(anchor="w", padx=10)

entry_frame = Frame(root)
entry_frame.pack(pady=5, padx=10, fill="x")

message_entry = Entry(entry_frame, width=40)
message_entry.pack(side=LEFT, padx=5, expand=True, fill="x")

send_button = Button(entry_frame, text="Envoyer", command=lambda: send_message())
send_button.pack(side=RIGHT, padx=5)

#envoie des messages
def send_message():
    message = message_entry.get()
    if message:
        client.send(bytes(message, "utf-8"))
        message_entry.delete(0, END)
        if message.lower() == "exit":
            client.close()
            root.quit()

#reception des messages
def receive_message():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            chat_area.config(state=NORMAL)
            chat_area.insert(END, message + "\n")
            chat_area.config(state=DISABLED)  
            chat_area.yview(END)  
        except:
            break

#thread pour recevoir les messages
thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()

root.mainloop()
