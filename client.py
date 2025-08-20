import tkinter as tk
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
import json


class Client:
    def __init__(self, window, host, port, username):
        self.window = window
        self.username = username

        text_font = ('JetBrains Mono', 10)
        fg = "#FAF9F6"
        list_box_bg = "#0F2A65"
        entry_bg = "#637DB5"
        button_bg = "#3B3E43"

        self.messageBox = tk.Listbox(
            window, height=20, width=100, bg=list_box_bg, fg=fg)
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg=entry_bg, fg=fg)
        self.msgEntry.pack()
        self.msgEntry.bind("<Return>", self.send_texts)  # Enter envia msg

        self.button = tk.Button(window, text="Send text", font=text_font,
                                width=20, bg=button_bg, fg=fg,
                                command=self.send_texts)
        self.button.pack()

        self.host = host
        self.port = port
        self.buffer = 1024
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        # Envia username logo após conectar
        self.sock.send(bytes(self.username, "utf8"))

        Thread(target=self.recv_texts, daemon=True).start()

    def recv_texts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                if not msg:
                    break
                self.messageBox.insert('end', msg)
                self.messageBox.yview(tk.END)  # Auto-scroll
            except OSError:
                break

    def send_texts(self, event=None):
        msg = self.msgEntry.get().strip()
        if msg:
            payload = json.dumps({"from": self.username, "msg": msg})
            self.sock.send(bytes(payload, "utf8"))
            self.msgEntry.delete(0, tk.END)


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Kawasha")

    # Pega username antes de abrir o chat
    username = input("Digite seu apelido: ")

    Client(window, "192.168.0.4", 8000, username)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
