
"""
Functions for the Virtual Credit Cards Server

startServer() - Starts listening the requests.
stopServer() - Closes the server if the server is open (basically it sends data and the server reacts and ends the loop of "sock.accept()" ).
getAccounts(fname) - Searchs every account into a file.

Account, the class Account represents a credit card Account.

"""

import socket
import threading
from pathlib import Path
import base64 as b64
from tkinter import *
from tkinter.messagebox import showerror

global accounts
accounts: "Account" = {}
ac_ip = {}

global ths
ths = {}

def startServer(method):
    """
    Starts the server and starts listening clients.
    """
    ths["server"] = {}

    ths["server"]["end"] = False
    def listen(method):
        sock = socket.socket()
        sock.bind(('127.7.7.88',7788))
        sock.listen(0)

        while ths["server"]["end"] == False:
            con,addr = sock.accept()
            
            req = con.recv(1024).decode().split("\n")
            for msg in req:
                res = method(msg,addr)
                if res.startswith("1"):
                    break

            con.send(res.encode())
                
            con.close()

        ths["server"]["end"] = False
    
    ths["server"]["th"] = threading.Thread(target=listen,args=[method])
    ths["server"]["th"].setDaemon(True)
    ths["server"]["th"].start()

def stopServer():
    """
    Stops the server. It sends data to the server and breaks the server's loop.
    """
    sock = socket.socket()
    
    try:
        sock.connect(('127.7.7.88',7788))
    except ConnectionRefusedError:
        return

    sock.send("end".encode())

    sock.close()

def getAccounts(name):
    """ 
    Gets all the accounts into a file.
    """

    if not Path(name).exists():
        return

    dectxt = b64.b64decode(Path(name).read_bytes()).decode()

    for ln in dectxt.split("\r\n"):
        Account(int(ln.split("|")[0]),ln.split("|")[1],ln.split("|")[2])

class Account:

    """
    Represents a account.
    Basically it's a account that has money, a cedula and a password.
    """

    money = 0
    cedula = "NONE"
    password = "NOPASSWORD"

    def __init__(self,_money = 0,_cedula = "NONE",_password = "NOPASSWORD"):
        self.money = _money
        self.cedula = _cedula
        self.password = _password
        accounts[self.cedula] = self

    def asString(self):
        return str(self.money)+"|"+self.cedula+"|"+self.password

    def moneyLess(self,amount):
        self.money -= amount
        accounts[self.cedula].money = self.money
        
    def moneyMore(self,amount):
        self.money += amount
        accounts[self.cedula].money = self.money

class AskAccount(Toplevel):

    modify = False
    amount = True

    def send(self):
        if self.response_c.get() == "" or not self.amount and self.response_p == "":
            return
        if self.modify:
            self.only_check_cedula()
            return
        if self.amount:
            self.callback(self.response_c.get())
            super().destroy()
            return

        sock = socket.socket()
        try:
            sock.connect(("127.7.7.88",7788))
        except ConnectionRefusedError:
            sock.close()
            showerror("Error","La App no pudo conectarse al servidor, intente mas tarde")
            return
        sock.send(f"""open {self.response_c.get()} {self.response_p.get()} false
less 0 {self.response_c.get()} {self.response_p.get()} false
close {self.response_c.get()} {self.response_p.get()} false""".encode())
        res = sock.recv(1024).decode()
        if res.startswith("1"):
            showerror("Error",res.split(":")[1])
            sock.close()
            self.destroy()
            return
        sock.close()

        self.callback(self.response_c.get()+"|"+self.response_p.get())
        super().destroy()

    def __init__(self,title,callback,**kwargs):
        in1text = "Cedula"
        in2text = "Contraseña"

        if kwargs.__contains__('input1text'):
            in1text = kwargs["input1text"]
        if kwargs.__contains__('input2text'):
            in2text = kwargs["input2text"]
        if kwargs.__contains__('modifiying'):
            self.modify = kwargs["modifiying"]

        super().__init__()

        self.callback = callback

        self.title(title)

        Label(self,text=in1text).pack(padx=8,pady=5,side=TOP)

        self.response_c = Entry(self)
        self.response_c.pack(padx=5,pady=(0,5),side=TOP)

        if not in2text == "":
            Label(self,text=in2text).pack(padx=8,pady=5,side=TOP)

            self.response_p = Entry(self)
            self.response_p.pack(padx=5,pady=(0,5),side=TOP)

            self.amount = False

        self.accept = Button(self,text="Aceptar",command=self.send)
        self.accept.pack(padx=5,pady=5,side=BOTTOM)

        self.focus()
        self.wait_window()

    def only_check_cedula(self):
        sock = socket.socket()
        
        try:
            sock.connect(("127.7.7.88",7788))
        except ConnectionRefusedError:
            sock.close()
            showerror("Error","La App no pudo conectarse al servidor, intente mas tarde")
            return
        
        try:
            sock.send(f"""open {self.response_c.get()} {accounts[self.response_c.get()].password} false
    less 0 {self.response_c.get()} {accounts[self.response_c.get()].password} false
    close {self.response_c.get()} {accounts[self.response_c.get()].password} false""".encode())
        except KeyError:
            showerror("Modificacion", "La cedula introducida no existe")
            return

        res = sock.recv(1024).decode()
        if res.startswith("1"):
            showerror("Error",res.split(":")[1])
            sock.close()
            self.destroy()
            return
        sock.close()

        self.callback(self.response_c.get()+"|"+self.response_p.get())
        super().destroy()

    def destroy(self):
        self.callback("")
        super().destroy()
