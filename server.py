import socket
import threading

IP = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

server.bind((IP, PORT))

server.listen(2)

clients = []
pseudos = []

def broadcast(message):
    for client in clients:
        client.send(bytes(message, "utf-8"))
        
def handle_connexion():
    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {str(address)}")
        
        pseudo = client.recv(1024).decode("utf-8")
        
        clients.append(client)
        pseudos.append(pseudo)
        
        print(f"{pseudo} a rejoint le chat !")
        client.send("Bienvenue sur le chat ! \n".encode("utf-8"))
        broadcast(f"{pseudo} a rejoint le chat !")
        
        thread = threading.Thread(target=handle_client, args=(client, pseudo))
        thread.start()

def handle_client(client, pseudo):
    while True:
        try :
            message = client.recv(1024).decode("utf-8")
            
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
