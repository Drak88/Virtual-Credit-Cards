
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
                method(msg,addr)

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
        Account(ln.split("|")[0],ln.split("|")[1],ln.split("|")[2])

class Account:

    """
    Represents a account.
    Basically it's a account that has money, a cedula and a password.
    """

    money = 0
    cedula = "NONE"
    password = "NOPASSWORD"

    def __init__(self,_money,_cedula,_password):
        self.setValues(_money,_cedula,_password)
        accounts[_cedula] = self

    def __str__(self):
        return str(self.money)+"|"+self.cedula+"|"+self.password

    def saveAsGlobal(self):
        for i in range(len(accounts)):
            if accounts[i].cedula == self.cedula:
                accounts[i].money = self.money
                accounts[i].password = self.password

    def setValues(self,_money = money,_cedula = cedula,_password = password):
        self.money = _money
        self.cedula = _cedula
        self.password = _password

