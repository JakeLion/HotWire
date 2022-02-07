#from os import stat
import socket
import threading
import tkinter
from tkinter import ttk
from tkinter.constants import PROJECTING
import tkinter.scrolledtext
from tkinter import simpledialog
import datetime
from datetime import *
import webbrowser

version = "1.0.0 ALPHA"

url = "https://jakesystems.us/"

HOST = '127.0.0.1'
PORT = 9090

class Client():

    #begins by creating connection to the server and requesting a nickname from the user
    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Enter a nickname", parent=msg)
        self.gui_done = False

        self.host1 = simpledialog.askstring("Server IP", "Enter a server IP", parent=msg)
        self.port1 = simpledialog.askinteger("Server port", "Enter a port", parent=msg)

        self.sock.connect((self.host1, self.port1))

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    #maintains and builds software UI
    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title(f"Hot-Wire Client {version} - {self.nickname}")
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat history:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=2)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.pack(padx=20, pady=5)

        
        self.support_button = tkinter.Button(self.win, text="Support", command=openBrowser)
        self.support_button.pack(padx=20, pady=5)

        #self.nick_show = tkinter.Label(self.win, text=f"You are {self.nickname}", bg="lightgray")
        #self.nick_show.pack(padx=2, pady=2)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    #handles transmission of messages to server
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    #shoots all processes in the head when user clicks X
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)
    
    #handles reception of new messages from server
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        self.text_area.config(state="normal")
                        self.text_area.insert('end', f"[{current_time}] {message}")
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break



def openBrowser():
    webbrowser.open("https://jakesystems.us/", new=2)

client = Client(HOST, PORT)


"""
- add webserver side to the server
- fix nickname error in the server
- set an icon for the UI of client
- reorganize the UI
- add a peer to peer capability for small conversations [Maybe]
- add a command system
- add a kick system
- add an ip blacklist (for bans)
- create a favorite servers list so users can easily recconect to servers they like
- create a connnected users list to see who is connected to each server
- add hotkeys like enter = send message
- add system where server automatically sets internal IP
- add way for users to download past messages
- add discord presence to the client

"""
