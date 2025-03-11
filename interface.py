from tkinter import *
from tkinter import scrolledtext

class ChatInterface:
    def __init__(self, send_callback):
        self.root = Tk()
        self.root.title("WhatsUp")
        self.root.geometry("500x400")

        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=WORD, state=DISABLED, width=60, height=15)
        self.chat_area.pack(pady=10, padx=10)

        self.pseudo_label = Label(self.root, text="Pseudo : ", font=("Arial", 10, "bold"))
        self.pseudo_label.pack(anchor="w", padx=10)

        entry_frame = Frame(self.root)
        entry_frame.pack(pady=5, padx=10, fill="x")

        self.message_entry = Entry(entry_frame, width=40)
        self.message_entry.pack(side=LEFT, padx=5, expand=True, fill="x")

        self.send_button = Button(entry_frame, text="Envoyer", command=lambda: send_callback(self.message_entry.get()))
        self.send_button.pack(side=RIGHT, padx=5)

    def update_pseudo(self, pseudo):
        self.pseudo_label.config(text=f"Pseudo : {pseudo}")

    def display_message(self, message):
        self.chat_area.config(state=NORMAL)
        self.chat_area.insert(END, message + "\n")
        self.chat_area.config(state=DISABLED)
        self.chat_area.yview(END)

    def clear_entry(self):
        self.message_entry.delete(0, END)

    def run(self):
        self.root.mainloop()