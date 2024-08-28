# Includes
from tkinter import *
from tkinter.messagebox import showerror,showwarning,showinfo

import base64 as b64
import pathlib as pl

import socket

# Vars
step = 0

amount = 0
cedula = ""
password = ""
destiny = ""
destinatories = ""

# Tkinter's magic
wnd = Tk()
wnd.title("Virtual Credit Cards")
wnd.geometry("157x269")

# It means description
des = Label(text="Monto (Bs)",font=("consolas",10))
des.place(x=5,y=1)

pant = Entry(width=23,fg="green",disabledforeground="green",disabledbackground="white",bg="white",state="normal")
pant.place(x=5,y=22)

pant.config(state="disabled")

# Methods
def getDestinatories():
    global destinatories
    
    if not pl.Path("destinatories.dt").exists():
        return

    destinatories = b64.b64decode(pl.Path("destinatories.dt").read_bytes()).decode()

def put(c):
    global step

    if step == 3:
        pant.config(state="normal")
        reset()
        return

    pant.config(state="normal")
    if c == "accept" and pant.get() == "":
#    It's used for testing, cause if you press accept button it will check if the server is
#    active or not. Line #101 only checks if there's a destinatory, this does the same but
#    at the end.
        try:
            sock = socket.socket()
            sock.connect(('127.7.7.88',7788))
            sock.send("exit".encode())
            if not sock.recv(1024):
                showerror("Error","VCC no puede conectarse al servidor, intente mas tarde")
        except ConnectionRefusedError:
            showerror("Error","VCC no puede conectarse al servidor, intente mas tarde")
        if c == "accept" and destiny == "":
            showwarning("Problema","Ningun destinatario ha sido previamente seleccionado, por favor selecciona uno. Si necesitas ayuda, consulta en la pagina: [PAGINA DE AYUDA]")
        reset()
        return
    if c == "backspace":
        if pant.get() == "" and step > 0:
            step -= 1

            if step == 0:
                reset()
            elif step == 1:
                pant.delete(0,END)
                des['text'] = "Cedula"

            pant.config(state="disabled")
            return
        pant.delete(len(pant.get())-1,END)
        return
    if c == "accept":
        accept()
        return
    pant.insert(END,c)
    pant.config(state="disabled")

def reset():
    global step,amount,cedula,password

    step = 0
    amount = 0
    cedula = ""
    password = ""
    pant.delete(0,END)
    pant.config(fg="green",disabledforeground="green",state="disabled",show="")
    des['text'] = "Monto (Bs)"

def accept():
    global step,amount,cedula,password

    if destiny == "" and not pant.get() == "0":
        showwarning("Problema","Ningun destinatario ha sido previamente seleccionado, por favor selecciona uno. Si necesitas ayuda, consulta en la pagina: [PAGINA DE AYUDA]")
        reset()
        return
    if step == 0:
        amount = pant.get()
        pant.delete(0,END)
        des['text'] = "Cedula"
        step = 1
        if amount == "0":
            DestineChooser()
            reset()
        return
    if step == 1:
        cedula = pant.get()
        pant.delete(0,END)
        pant.configure(show="*")
        des['text'] = "Contraseña"
        step = 2
        return
    if step == 2:
        password = pant.get()
        pant.delete(0,END)
        
        sockm = socket.socket()
        try:
            sockm.connect(("127.7.7.88",7788))
        except ConnectionRefusedError:
            showerror("Error","VCC no puede conectarse al servidor, intente mas tarde")
            reset()
            return
        sockm.send(f"""open {cedula} {password} false
less {amount} {cedula} {password} true
close {cedula} {password} false""".encode())
        res = sockm.recv(1024).decode()
        if res.startswith("1") and ":" in res:
            pant.config(state="normal",disabledforeground="red",show="")
            pant.delete(0,END)
            pant.insert(0,res.split(":")[1])
            pant.config(state="disabled")
            sockm.close()
            step = 3
            return
        sockm.close()

        sockp = socket.socket()
        try:
            sockp.connect(("127.7.7.88",7788))
        except ConnectionRefusedError:
            showerror(title="Error",message="VCC no puede conectarse al servidor, intente mas tarde")
            reset()
            return
        sockp.send(f"""open {destiny.split("|")[0]} {destiny.split("|")[1]} false
more {amount} {destiny.split("|")[0]} {destiny.split("|")[1]} true
close {destiny.split("|")[0]} {destiny.split("|")[1]} false""".encode())
        res = sockp.recv(1024).decode()
        if res.startswith("1"):
            showerror("Error",res.split(":")[1])
            sockp.close()
            return
        sockp.close()

        showinfo("Mensaje","Transaccion realizada satisfactoriamente")

        reset()
        return

# Classes

class AskAccount(Toplevel):

    def send(self):

        if self.response_c.get() == "" or self.response_p.get() == "":
            return

        sock = socket.socket()
        try:
            sock.connect(("127.7.7.88",7788))
        except ConnectionRefusedError:
            sock.close()
            showerror("Error","La App no pudo conectarse al servidor, intente mas tarde")
            reset()
            return
        sock.send(f"""open {self.response_c.get()} {self.response_p.get()} true
less 0 {self.response_c.get()} {self.response_p.get()} true
close {self.response_c.get()} {self.response_p.get()} true""".encode())
        res = sock.recv(1024).decode()
        if res.startswith("1"):
            showerror("Error",res.split(":")[1])
            sock.close()
            self.destroy()
            return
        sock.close()

        self.callback(self.response_c.get()+"|"+self.response_p.get())
        super().destroy()

    def __init__(self,title,callback,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.callback = callback

        self.title(title)

        Label(self,text="Cedula").pack(padx=8,pady=5,side=TOP)

        self.response_c = Entry(self)
        self.response_c.pack(padx=5,pady=(0,5),side=TOP)

        Label(self,text="Contraseña").pack(padx=8,pady=5,side=TOP)

        self.response_p = Entry(self)
        self.response_p.pack(padx=5,pady=(0,5),side=TOP)

        self.accept = Button(self,text="Aceptar",command=self.send)
        self.accept.pack(padx=5,pady=5,side=BOTTOM)

        self.focus()
        self.grab_set()
        self.wait_window()

    def destroy(self):
        self.callback("")
        super().destroy()

class DestineChooser(Toplevel):

    local_destinatories = None
    selected = None
    response = ""

    def getResponse(self,response):
        self.response = response

    def createDestine(self):
        global destinatories

        AskAccount("Pedir cuenta",self.getResponse)

        if destinatories == "":
            destinatories = self.response
        else:
            destinatories += "\n"+self.response

        self.des_list.insert(END,self.response.split("|")[0])

        pl.Path("destinatories.dt").write_bytes(b64.b64encode(destinatories.encode()))

    def removeDestine(self):
        if not self.selected:
            return
        global destinatories

        destinatories = destinatories.replace(self.selected+"|"+destinatories[destinatories.find(self.selected):].split("|")[1].split("\n")[0],"").replace("\n\n","\n")

        self.des_list.delete(0,END)
        for ln in destinatories.split("\r\n"):
                self.des_list.insert(END,ln.split("|")[0])

    def select(self,event):
        self.selected = event.widget.get(ANCHOR)

    def accept(self):
        if not self.selected:
            return
        global destiny
        destiny = self.selected+"|"+destinatories[destinatories.rfind(self.selected):].split("|")[1].split("\n")[0]
        self.destroy()

    def cancelOption(self):
        global destinatories
        destinatories = self.local_destinatories
        self.destroy()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.local_destinatories = destinatories

        self.title("Elegir destinatario")

        Label(self,text="Destinatarios",justify=LEFT,font=("MS Reference Sans Serif",18)).pack(padx=5,pady=(5,0),fill=BOTH,side=TOP)

        self.des_list = Listbox(self)
        self.des_list.bind("<<ListboxSelect>>",self.select)
        self.des_list.pack(padx=5,pady=(5,0),fill=BOTH,expand=True)

        if not destinatories == "":
            for ln in destinatories.split("\n"):
                self.des_list.insert(END,ln.split("|")[0])

        self.add = Button(self,text="+",command=self.createDestine)
        self.add.pack(padx=5,pady=(5,20),fill=BOTH,side=RIGHT,expand=True)
        
        self.remove = Button(self,text="-",command=self.removeDestine)
        self.remove.pack(padx=5,pady=(5,20),fill=BOTH,side=RIGHT,expand=True)

        buttons = Frame(self)

        self.accept = Button(buttons,text="Aceptar",command=self.accept)
        self.accept.pack(padx=5,pady=5,side=BOTTOM,fill=BOTH,expand=True)

        self.cancel = Button(buttons,text="Cancelar",command=self.cancelOption)
        self.cancel.pack(padx=5,pady=5,side=BOTTOM,fill=BOTH,expand=True)

        buttons.pack(side=BOTTOM,fill=BOTH,expand=True)

        self.focus()
        self.grab_set()

# Tkinter's magic again

# Not the music band named BTS, it means "Buttons"
bts = {}

bts['7'] = Button(text="7",width=6,height=3,command= lambda: put("7"))
bts['8'] = Button(text="8",width=6,height=3,command= lambda: put("8"))
bts['9'] = Button(text="9",width=6,height=3,command= lambda: put("9"))

bts['4'] = Button(text="4",width=6,height=3,command= lambda: put("4"))
bts['5'] = Button(text="5",width=6,height=3,command= lambda: put("5"))
bts['6'] = Button(text="6",width=6,height=3,command= lambda: put("6"))

bts['1'] = Button(text="1",width=6,height=3,command= lambda: put("1"))
bts['2'] = Button(text="2",width=6,height=3,command= lambda: put("2"))
bts['3'] = Button(text="3",width=6,height=3,command= lambda: put("3"))

bts['backspace'] = Button(text="<",width=6,height=3,fg="orange",command= lambda: put("backspace"))
bts['0'] = Button(text="0",width=6,height=3,command= lambda: put("0"))
bts['accept'] = Button(text="√",width=6,height=3,fg="green",command= lambda: put("accept"))

bts["1"].grid(row=1,column=0,pady=(45,0))
bts["2"].grid(row=1,column=1,pady=(45,0))
bts["3"].grid(row=1,column=2,pady=(45,0))

bts["4"].grid(row=2,column=0)
bts["5"].grid(row=2,column=1)
bts["6"].grid(row=2,column=2)

bts["7"].grid(row=3,column=0)
bts["8"].grid(row=3,column=1)
bts["9"].grid(row=3,column=2)

bts["backspace"].grid(row=4,column=0)
bts["0"].grid(row=4,column=1)
bts["accept"].grid(row=4,column=2)

getDestinatories()

wnd.resizable(False,False)
wnd.mainloop()
