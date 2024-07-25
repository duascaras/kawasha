from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.client = {}
        self.addrs = {}

    def serverStart(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("We are on!")

        while True:
            try:
                cliSock, cliAddr = self.sock.accept()
                print(f"Con received from {cliAddr}.")

                self.client[cliSock] = cliAddr
                self.addrs[cliAddr] = cliAddr

                Thread(target=self.handling, args=(cliSock,)).start()
            except Exception as e:
                print(f"{e} Con closed")

    def handling(self, cliSock):
        while True:
            msg = cliSock.recv(self.buffer).decode("utf8")
            print(cliSock)
            if msg:
                print(f"{msg} received.")
                self.sendText(msg)

    def sendText(self, msg):
        for sock in self.clients:
            try:
                sock.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    try:
        Server("localhost", 8000).serverStart()
    except KeyboardInterrupt:
        print(" <- Closed Con")
