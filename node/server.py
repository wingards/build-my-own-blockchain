
import zmq
import time
import threading

class Server_Interface:
    def __init__(self, host = '0.0.0.0', port = 9527):
        context = zmq.Context()
        self.server = context.socket(zmq.REP)
        self.server.bind("tcp://%s:%s" % (host, port))

        self.message_queue = []

    def _response(self, recv):
        self.server.send(recv)

    def _listen(self):
        while True:
            recv = self.server.recv()
            print("Recv:{}".format(recv.decode()))

            self._response(recv)

            if recv.decode() == "End":
                break

            self.message_queue.append(recv.decode())

        print("Server Exit")

    def listen(self):
        thread = threading.Thread(target = self._listen, args = ())
        thread.start()

    def query_message(self):

        if not self.message_queue:
            return ""

        return self.message_queue[0]

class Server_Test(Server_Interface):



    pass

if __name__ == "__main__":
    server = Server_Test()
    server.listen()
