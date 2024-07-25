import tkinter as tk
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


class Client():
    def __init__(self, window, host, port):
        self.window = window

        text_font = ('JetBrains Mono', 10)
        # fg = text color
        fg = "#FAF9F6"
        list_box_bg = "#0F2A65"
        entry_bg = "#637DB5"
        button_bg = "#3B3E43"

        self.messageBox = tk.Listbox(
            window, height=20, width=100, bg=list_box_bg, fg=fg)
        self.messageBox.pack()

        self.msgEntry = tk.Entry(window, width=100, bg=entry_bg, fg=fg)
        self.msgEntry.pack()

        self.button = tk.Button(window, text="Send text", font=text_font,
                                width=20, bg=button_bg, fg=fg,
                                highlightbackground=entry_bg,
                                command=self.send_texts)
        self.button.pack()

        self.host = host
        self.port = port
        self.buffer = 1024
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((self.host, self.port))

        Thread(target=self.recv_texts).start()

    def recv_texts(self):
        while True:
            try:
                msg = self.sock.recv(self.buffer).decode("utf8")
                self.messageBox.insert('end', msg)
            except OSError:
                break

    def send_texts(self):
        self.sock.send(bytes(self.msgEntry.get(), "utf8"))


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Kawasha")
    Client(window, "localhost", 8000)
    try:
        window.mainloop()
    except KeyboardInterrupt:
        window.destroy()
