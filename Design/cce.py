import tkinter as tk
from tkinter import *
import mysql.connector as mysql
from tkinter import ttk, messagebox

db=mysql.connect(host="localhost",user="root",password="5877",database="typ")
mycursor=db.cursor()

cc=Tk()
cc.title("SafarCard")
cc.geometry("2700x1900")
cc.config(background="white")
def add():
    frame=Frame(cc,background="grey",width=1500,height=800)
    frame.grid(row=1,column=0,sticky=NW,padx=20)
    Label(frame,text=" ",font=("Times New Roman",14),background="grey",foreground="black").grid(row=0,column=0,sticky=W,pady=10)  
    Label(frame,text="Name",font=("Times New Roman",14),background="grey",foreground="black").grid(row=1,column=0,sticky=W,pady=10)  
    Label(frame,text="SafarCard number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=2,column=0,sticky=W,pady=10)
    Label(frame,text="Phone number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=3,column=0,sticky=W,pady=10)
    Label(frame,text="E-Mail ID",font=("Times New Roman",14),background="grey",foreground="black").grid(row=4,column=0,sticky=W,pady=10)
    Label(frame,text="Aadhar number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=5,column=0,sticky=W,pady=10)
    Label(frame,text="SafarCard Account Balance",font=("Times New Roman",14),background="grey",foreground="black").grid(row=6,column=0,sticky=W,pady=10)
    
    name=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    cardno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    phno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    eid=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    adharno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    balance=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    
    name.grid(row=1,column=1)
    cardno.grid(row=2,column=1)
    phno.grid(row=3,column=1)
    eid.grid(row=4,column=1)
    adharno.grid(row=5,column=1)
    balance.grid(row=6,column=1)
    def submituser():
        namee=name.get()
        cardnoe=int(cardno.get())
        phnoe=phno.get()
        emaile=eid.get()
        adharnoe=adharno.get()
        balancee=int(balance.get())
        print(namee,cardnoe,phnoe,emaile,adharnoe,balancee)
        sql="insert into typ.user values('%s',%d,'%s','%s','%s',%d)"%(namee,cardnoe,phnoe,emaile,adharnoe,balancee)
        c=mycursor.execute(sql)
        print(c)
        db.commit()
    Button(frame,text="Add",command=submituser,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=7, column=1,pady=40)
    

def delete():
    fram=Frame(cc,background="grey",width=1500,height=800)
    fram.grid(row=1,column=0,sticky=N)
    Label(fram,text="""
    """,background="grey",font=("Times New Roman",14)).grid(row=0,column=0)
    Label(fram,text="SafarCard number ",background="grey",font=("Times New Roman",14)).grid(row=1,column=0)
    cardno=Entry(fram,font=("Times New Roman",14),foreground="black")
    cardno.grid(row=1,column=1)
    def deleteuser():
        cardnoe=int(cardno.get())

        sql="delete from typ.user where cardno=%d"%cardnoe
        c=mycursor.execute(sql)
        print(c)
        db.commit()
    Button(fram,text="Delete",command=deleteuser,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=2, column=1,pady=40)
    
    
def update():
    frame=Frame(cc,background="grey",width=1500,height=800)
    frame.grid(row=1,column=0,sticky=NE)
    Label(frame,text=" ",font=("Times New Roman",14),background="grey",foreground="black").grid(row=0,column=0,sticky=W,pady=10)  
    Label(frame,text="Name",font=("Times New Roman",14),background="grey",foreground="black").grid(row=1,column=0,sticky=W,pady=10)  
    Label(frame,text="SafarCard number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=2,column=0,sticky=W,pady=10)
    Label(frame,text="Phone number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=3,column=0,sticky=W,pady=10)
    Label(frame,text="E-Mail ID",font=("Times New Roman",14),background="grey",foreground="black").grid(row=4,column=0,sticky=W,pady=10)
    Label(frame,text="Aadhar number",font=("Times New Roman",14),background="grey",foreground="black").grid(row=5,column=0,sticky=W,pady=10)
    Label(frame,text="SafarCard Account Balance",font=("Times New Roman",14),background="grey",foreground="black").grid(row=6,column=0,sticky=W,pady=10)
    name=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    cardno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    phno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    eid=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    adharno=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    balance=Entry(frame,background="white",font=("Times New Roman",14),foreground="black")
    
    name.grid(row=1,column=1)
    cardno.grid(row=2,column=1)
    phno.grid(row=3,column=1)
    eid.grid(row=4,column=1)
    adharno.grid(row=5,column=1)
    balance.grid(row=6,column=1)
    def submituser():
        namee=name.get()
        cardnoe=int(cardno.get())
        phnoe=phno.get()
        emaile=eid.get()
        adharnoe=adharno.get()
        balancee=int(balance.get())
        
        sql="update typ.user set name='%s',phno='%s',email='%s',adharno='%s',balance=%d where cardno=%d"%(namee,phnoe,emaile,adharnoe,balancee,cardnoe)
        c=mycursor.execute(sql)
        print(c)
        db.commit()
    Button(frame,text="Update",command=submituser,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=7, column=1,pady=40)
    

    
cce=Frame(cc,background="white")
cce.grid(row=0,column=0)

Label(cce,text="SafarCard",font=("Times New Roman",30,"bold"),background="white",foreground="black").grid(row=0,column=1,padx=20,pady=20)
Button(cce,text="Add User",command=add,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=1, column=0,pady=40)
Button(cce,text="Delete User",command=delete,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=1, column=1,pady=40)
Button(cce,text="Update User",command=update,height=1,width=10,font=("Times New Roman",14,"bold"),foreground="black").grid(row=1, column=2,pady=40)
frame=Frame(cc,background="grey",width=1300,height=800)
frame.grid(row=1,column=0,padx=20)
add()
delete()
update()
cce.mainloop()
   
  
    