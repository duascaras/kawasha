import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Lock


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.buffer = 1024
        self.clients = {}  # sock -> username
        self.lock = Lock()

    def server_start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server started!")

        while True:
            try:
                cli_sock, cli_addr = self.sock.accept()
                print(f"Con received from {cli_addr}.")
                Thread(target=self.handling, args=(
                    cli_sock,), daemon=True).start()
            except Exception as e:
                print(f"{e} Con closed")

    def handling(self, cli_sock):
        try:
            # Primeiro pacote recebido deve ser o username
            username = cli_sock.recv(self.buffer).decode("utf8")
            with self.lock:
                self.clients[cli_sock] = username

            self.send_text(f"🔵 {username} entrou no chat")

            while True:
                data = cli_sock.recv(self.buffer).decode("utf8")
                if not data:
                    break

                msg = json.loads(data)
                print(f"[{msg['from']}] {msg['msg']}")
                self.send_text(f"{msg['from']}: {msg['msg']}")

        except Exception as e:
            print(f"Erro: {e}")
        finally:
            with self.lock:
                username = self.clients.get(cli_sock, "Desconhecido")
                del self.clients[cli_sock]
            cli_sock.close()
            self.send_text(f"🔴 {username} saiu do chat")

    def send_text(self, msg):
        with self.lock:
            for sock in list(self.clients.keys()):
                try:
                    sock.send(bytes(msg, "utf8"))
                except Exception as e:
                    print(f"Erro ao enviar msg: {e}")


if __name__ == "__main__":
    try:
        Server("0.0.0.0", 8000).server_start()
    except KeyboardInterrupt:
        print(" <- SERVER CLOSED.")
