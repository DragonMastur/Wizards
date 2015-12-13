import socket, select, pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 4000))
server.listen(5)

clients = []
LoginUsers = []
while True:
    Connections, wlist, xlist = select.select([server], [], [], 0.05)

    for Connection in Connections:
        client, Informations = Connection.accept()
        clients.append(client)

    clientsList = []
    try:
        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
    except select.error:
        pass
    else:
        for clientInList in clientsList:
            try:
                e='';data = clientInList.recv(1024)
                data = pickle.loads(data)
                print(data)
                if data.startswith("Login from '") and data.endswith("';"):
                    d = list(data)
                    for x in range(12):
                        d.pop(0)
                    d.pop(len(d)-1);d.pop(len(d)-1)
                    for i in d:
                        e+=i
                    if e not in LoginUsers:
                        LoginUsers.append(e)
                    else:
                        print("User '"+e+"' already loged in.")
                        data = "Your already loged in."
                if data.startswith("Disconnent from '") and data.endswith("';"):
                    d = list(data)
                    for x in range(12):
                        d.pop(0)
                    d.pop(len(d)-1);d.pop(len(d)-1)
                    for i in d:
                        e+=i
                    if e in LoginUsers:
                        LoginUsers.pop(LoginUsers.index(e))
                    else:
                        print("User '"+e+"' not loged in.")
                        data = "You are already loged out."
                data = pickle.dumps(data)
                clientInList.send(data)
            except KeyboardInterrupt:
                server.close()
                clientInList.close()
            except:
                pass

clientInList.close()
server.close()
