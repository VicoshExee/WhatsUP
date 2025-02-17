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

#interface
root = Tk()
root.title("Client Chat")
root.geometry("500x400")

chat_area = scrolledtext.ScrolledText(root, wrap=WORD, state=DISABLED, width=60, height=15)
chat_area.pack(pady=10)


message_entry = Entry(root, width=50)
message_entry.pack(pady=5)


def send_message():
    message = message_entry.get()
    if message:
        client.send(bytes(message, "utf-8"))
        message_entry.delete(0, END)  
        if message.lower() == "exit":
            client.close()
            root.quit()

send_button = Button(root, text="Envoyer", command=send_message)
send_button.pack(pady=5)

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

thread_receive = threading.Thread(target=receive_message, daemon=True)
thread_receive.start()

root.mainloop()
