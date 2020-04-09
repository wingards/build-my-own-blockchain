
from . import server, client

class Node_Interface:
    def __init__(self, host = '0.0.0.0', port = 9527):
        self.server = server.Server_Interface(host, port)
        self.client = client.Client_Interface()

    def connect(self, host, port):
        self.client.connect(host, port)

    def disconnect(self, host, port):
        self.client.disconnect(host, port)

    def list_connect(self):
        return self.client.connect_check

    def broadcast_message(self, message):
        self.client.broadcast_message(message)

    def listen(self):
        self.server.listen()

    def query_message(self):
        return self.server.query_message()

class Node_Test(Node_Interface):
    def __init__(self):
        self.server = server.Server_Test()
        self.client = client.Client_Test()

    def run_test(self):
        self.client.run_test()

if __name__ == "__main__":
    node = Node_Test()

    node.listen()

    node.connect('127.0.0.1', 9527)
    node.run_test()
