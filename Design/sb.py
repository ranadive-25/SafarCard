from tkinter import *
#from tkinter import ttk
import ttkbootstrap as ttk
root=ttk.Window(themename="sandstone")
root.geometry("500x400")
def here():
    root.withdraw()
    global ttk
    r=ttk.Toplevel()
    ttk.Button(r,text="done",command="here").place(x=50,y=100)
ttk.Button(root,text="done",command=here).place(x=50,y=100,anchor="center")
root.mainloop()