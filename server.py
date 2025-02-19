import socket
import threading
from chiffrement import *
IP = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(2)

clients = []
pseudos = []

#chiffrement César
def cesar_chiffrement(text, shift=3):  # mettre la clé pas en publique 
    result = ""
    for caractere in text:
        if caractere.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(caractere.lower()) - 97 + shift_amount) % 26) + 97)
            result += new_char.upper() if caractere.isupper() else new_char
        else:
            result += caractere
    return result

#déchiffrement César
def cesar_dechiffrement(text, shift=3):
    return cesar_chiffrement(text, -shift)


# Fonction de chiffrement Vigenère
def vigenere_cipher(text, key):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 + shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 + shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result

# Fonction de déchiffrement Vigenère
def vigenere_decipher(text, key):
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)].lower()) - 97
            if char.isupper():
                result += chr(((ord(char) - 65 - shift) % 26) + 65)
            else:
                result += chr(((ord(char) - 97 - shift) % 26) + 97)
            key_index += 1
        else:
            result += char
    return result



# Chiffrement global : César suivi de Vigenère
def encrypt(text, caesar_shift=3, vigenere_key="KEY"):
    text_cesar = cesar_chiffrement(text, caesar_shift)
    text_vigenere = vigenere_cipher(text_cesar, vigenere_key)
    return text_vigenere

# Déchiffrement global : Vigenère suivi de César
def decrypt(text, caesar_shift=3, vigenere_key="KEY"):
    text_vigenere = vigenere_decipher(text, vigenere_key)
    text_cesar = cesar_dechiffrement(text_vigenere, caesar_shift)
    return text_cesar


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
                index = clients.index(client)
                clients.remove(client)
                client.close()

                pseudo = pseudos[index]
                pseudos.remove(pseudo)

                broadcast(f"{pseudo} a quitté le chat !")
                break
            else:
                broadcast(f"{pseudo}: {message}")
        
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            pseudo = pseudos[index]
            pseudos.remove(pseudo)

            broadcast(f"{pseudo} a quitté le chat !")
            break

print("Le serveur est en marche !")
handle_connexion()
