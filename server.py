import socket, pickle

class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(('127.0.0.1', 4000))
	
    def send(self, data):
        data = pickle.dumps(data)
        self.server.send(data)
        data = self.server.recv(1024)
        data = pickle.loads(data)
        return data

    def close(self):
        server.close()
