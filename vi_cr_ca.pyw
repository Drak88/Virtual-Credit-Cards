# Includes
from tkinter import *

import socket

# Vars
step = 0

amount = 0
cedula = ""
password = ""
config = '''
*Configs*
'''

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
def put(c):

    pant.config(state="normal")
    if c == "backspace":
        pant.delete(len(pant.get())-1,END)
        return
    if c == "accept":
        accept()
        return
    if step == 1 and len(pant.get()) == 8:
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
    pant.config(state="disabled",show="")
    des['text'] = "Monto (Bs)"

def accept():
    global step,amount,cedula,password

    if step == 0:
        amount = pant.get()
        pant.delete(0,END)
        des['text'] = "Cedula"
        step = 1
        if amount != "0":
            pant.config(state="disabled")
        return
    if step == 1 and len(pant.get()) == 8 or pant.get() == "config":
        cedula = pant.get()
        pant.delete(0,END)
        pant.configure(show="*")
        des['text'] = "Contraseña"
        step = 2
        if cedula == "config":
            # Poner ventana de configuraciones
            reset()
        pant.config(state="disabled")
        return
    if step == 2:
        password = pant.get()
        pant.delete(0,END)
        
        sock = socket.socket()
        sock.connect(("127.7.7.88",7788))
        sock.send(f"""open {cedula} {password}
less {amount} {cedula} {password}
close {cedula} {password}""".encode())
        sock.close()

        reset()
        return

# Tkinter's magic again

# No the music band named BTS, it means "Buttons"
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

wnd.resizable(False,False)
wnd.mainloop()
