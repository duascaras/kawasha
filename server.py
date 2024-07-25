from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Server():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.client = {}

    def server_start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server started!")

        while True:
            try:
                cli_sock, cli_addr = self.sock.accept()
                print(f"Con received from {cli_addr}.")

                self.client[cli_sock] = cli_addr
                # self.addrs[cli_addr] = cli_addr

                # Thread(target=self.handling, args=(cli_sock,)).start()
                Thread(target=self.handling, args=(
                    cli_sock,), daemon=True).start()

            except Exception as e:
                print(f"{e} Con closed")

    def handling(self, cli_sock):
        while True:
            try:
                msg = cli_sock.recv(self.buffer).decode("utf8")
                if not msg:
                    break

                print(f"Message received from {self.client[cli_sock]}: {msg}.")
                self.send_text(f"{self.client[cli_sock]} says: {msg}")

            except OSError:
                break

        print(f"Client {self.client[cli_sock]} disconnected")
        del self.client[cli_sock]
        cli_sock.close()

    def send_text(self, msg):
        for sock in self.client.keys():
            try:
                sock.send(bytes(msg, "utf8"))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    try:
        server = Server("localhost", 8000).server_start()
        server.server_start()
    except KeyboardInterrupt:
        print(" <- SERVER CLOSED.")
