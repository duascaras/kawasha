import tkinter as tk
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Client():
    def __init__(self, window, host, port):
        self.window = window

        self.messageBox = tk.Listbox(
            window, height=20, width=100, bg="#fc6c85")
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg="fc6c85", fg="#000000")
        self.msgEntry.pack()

        self.button = tk.Button(window, text="Send text",
                                width=50, bg="fc6c85", command=self.senfTexts)
        self.button.pack()

        self.host = host
        self.port = port
        self.buffer = 1024
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        Thread(target=self.recvTexts).start()

    def recvTexts(self):
        while True:
            try:
                msg = self.rock.recv(self.buffer).decode("utf8")
                self.messageBox.insert(msg)
            except OSError:
                break

    def sendTexts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Simples chat app in tkinter")
    Client(window, "localhost", 8000)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
