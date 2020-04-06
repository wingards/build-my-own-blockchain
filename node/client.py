
import zmq
import time
import threading

class Client_Interface:
    def __init__(self):
        self.connections = []
        self.connect_check = []

    def connect(self, host, port):

        #check duplicated connection
        if (host, port) in self.connect_check:
            print("{}:{} already connected".format(host, port))
            return

        context = zmq.Context()
        client = context.socket(zmq.REQ)
        client.connect("tcp://%s:%s" % (host, port))

        self.connections.append(client)
        self.connect_check.append((host, port))

    def disconnect(self, host, port):
        index = self.connect_check.index((host, port))

        self.connections.pop(index)
        self.connect_check.pop(index)

    def send_message(self, connect_id, message):
        conn = self.connections[connect_id]

        print("Send Message {} To {}".format(message, conn))
        conn.send(message.encode('utf-8'))

    def wait_recieve(self, connect_id):
        recv = self.connections[connect_id].recv()
        return recv.decode('utf-8')

    def broadcast_message(self, message):

        recvs = []

        if not self.connections:
            print("Broadcast message fail: No Connections")
            return recvs

        for i in range(len(self.connections)):
            self.send_message(i, message)
            recvs.append(self.wait_recieve(i))

        print("Response:{}".format(recvs))

        return recvs

class Client_Test(Client_Interface):

    def run_test(self):

        for i in range(5):

            msg = "({}:{})".format(i, threading.get_ident())

            recvs = self.broadcast_message(msg)
            
            print(recvs)
            time.sleep(1)

        self.broadcast_message("End")

if __name__ == "__main__":
    client = Client_Test()
    client.connect('127.0.0.1', 9527)
    client.run_test()

    print(client.connections)
