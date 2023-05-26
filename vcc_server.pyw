from tkinter import *
from tkinter import ttk
import funcs_s as funcs

import base64 as b64
from pathlib import Path

# Accounts
funcs.getAccounts("acs.dt")

wnd = Tk()
wnd.title("Virtual Credit Cards Server")
wnd.geometry("400x400")

# Classes
class NewAccount(Toplevel):

    """A window for create an Account"""

    def __init__(self,*args,callback=None,**kwargs):
        super().__init__(*args,**kwargs)
        self.callback = callback
        self.config(width=600,height=200)
        self.title("Crear cuenta")

        self.tag0 = Label(self,text="Saldo")
        self.tag0.pack(fill=X,padx=5,pady=(2.5,1))

        self.money = Entry(self)
        self.money.pack(fill=BOTH,expand=1,padx=5,pady=2.5)
        
        self.tag1 = Label(self,text="Cedula")
        self.tag1.pack(fill=X,padx=5,pady=(2.5,1))

        self.cedula = Entry(self)
        self.cedula.pack(fill=BOTH,expand=1,padx=5,pady=2.5)
        
        self.tag2 = Label(self,text="Contraseña")
        self.tag2.pack(fill=X,padx=5,pady=(2.5,1))

        self.password = Entry(self)
        self.password.pack(fill=BOTH,expand=1,padx=5,pady=2.5)

        self.acb = Button(self,text="Aceptar",command=self.send)
        """Accept button"""
        self.acb.pack(fill=BOTH,expand=1,padx=5,pady=2.5)

        self.focus()
        self.grab_set()

    def send(self):
        cnt = self.verificate({"mn":self.money.get(),"cdl":self.cedula.get(),"psw":self.password.get()})
        
        if cnt['prb'] == False:
            self.callback(self.money.get(),self.cedula.get(),self.password.get())
            super().destroy()
        else:
            self.tag0['text'] = cnt['mn']
            self.tag1['text'] = cnt['cdl']
            self.tag2['text'] = cnt['psw']

    def verificate(self,cnt: "dict[str,str,str]"):
        prbs: "dict[str,str,str,bool]" = {"mn":"Saldo","cdl":"Cedula","psw":"Contraseña","prb":False}
        """ Problems """
        if not cnt['mn'].isdigit() or cnt['mn'].isdigit() and int(cnt['mn']) < 0:
            prbs['mn'] = "Saldo, cantidad invalida"
            prbs['prb'] = True
        if not cnt['cdl'].isdigit() or len(cnt['cdl']) == 0:
            prbs['cdl'] = "Cedula, ID invalido"
            prbs['prb'] = True
        if not cnt['psw'].isdigit():
            prbs['psw'] = "Contraseña, contraseña no valida"
            prbs['prb'] = True
        elif len(cnt['psw']) <= 4:
            prbs['psw'] = "Contraseña, la contraseña debe tener mas de 4 caracteres"
            prbs['prb'] = True

        if cnt['cdl'] in funcs.accounts:
            prbs['cdl'] += ", cedula ya existente"
            prbs['prb'] = True
        
        return prbs

    def destroy(self):
        self.callback("NO","NO","NO")
        super().destroy()

class AccountsTV(ttk.Frame):
    """ Accounts - TreeView """

    def __init__(self,*args,**kwargs):
        super().__init__(*args,*kwargs)
		# acssb = Accounts Scrollbar | acs = Accounts
        self.acssbh = ttk.Scrollbar(self,orient=HORIZONTAL)
        self.acssbv = ttk.Scrollbar(self,orient=VERTICAL)
        self.acs = ttk.Treeview(self,xscrollcommand=self.acssbh.set,yscrollcommand=self.acssbv.set)
        self.acssbh.config(command=self.acs.xview)
        self.acssbh.pack(side=BOTTOM,fill='x')
        self.acssbv.config(command=self.acs.yview)
        self.acssbv.pack(side=RIGHT,fill='y')
        self.acs.pack(fill='both',side=LEFT,padx=10,pady=(50,10))

# Methods
def loadAccounts():
    acs.acs.delete(*acs.acs.get_children())
    for ac in funcs.accounts:
        acs.acs.insert("",END,values=(funcs.accounts[ac].money,funcs.accounts[ac].cedula,funcs.accounts[ac].password))

def newAccount(event=None):
    data = {}
    def callback(mn,cd,ps):
        if mn == "NO" and cd == "NO" and ps == "NO":
            return
        data['money'] = mn
        data['cedula'] = cd
        data['password'] = ps
        funcs.Account(int(data['money']),data['cedula'],data['password'])
        loadAccounts()
    nwnd = NewAccount(callback=callback)

def on_request(msg,addr):
    req = msg.split(" ")

    if msg == "exit":
        return

    if req[0] == "open":
        if funcs.accounts[req[1]].password == req[2]:
            funcs.ac_ip[req[1]] = addr[0]

    if req[0] == "close":
        if funcs.accounts[req[1]].password == req[2] and req[1] in funcs.ac_ip:
            funcs.ac_ip.pop(req[1])

    if req[0] == "less":
        if funcs.accounts[req[2]].password == req[3] and req[2] in funcs.ac_ip:
            funcs.accounts[req[2]].money -= int(req[1])

    if req[0] == "more":
        if funcs.accounts[req[2]].password == req[3] and req[2] in funcs.ac_ip:
            funcs.accounts[req[2]].money += int(req[1])

    loadAccounts()

# Tkinter's magic again

acs = AccountsTV()
acs.acs.config(columns=("money","cedula","password"),show="headings")
acs.acs.heading("money",text="Saldo")
acs.acs.heading("cedula",text="Cedula")
acs.acs.heading("password",text="Contraseña")
acs.pack()

menubar = Menu(wnd)

accounts = Menu(menubar,tearoff=False)

accounts.add_command(
    label="Nueva",
    accelerator="Ctrl+N",
    command=newAccount
)
wnd.bind_all(sequence="<Control-n>",func=newAccount)

menubar.add_cascade(menu=accounts,label="Cuentas")

acslb = Label(wnd,text="Cuentas",font=("Sans-serif",16))
acslb.place(x=8,y=10)

loadAccounts()
funcs.startServer(on_request)

wnd.config(menu=menubar)
wnd.mainloop()

funcs.ths["server"]["end"] = True
funcs.stopServer()

lines: str = ""
for i in funcs.accounts:
    lines += funcs.accounts[i].__str__()+"\r\n"

if len(lines) > 0:
    lines = lines[:-2]
    Path("acs.dt").write_bytes(b64.b64encode(lines.encode()))
