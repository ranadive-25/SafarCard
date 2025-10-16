from tkinter import *
import tkinter as tk
import mysql.connector as mysql
from tkinter import messagebox
import ttkbootstrap as ttk
#connect to mysql workbench 
db=mysql.connect(host="localhost",user="root",password="5877",database="safarcard")
mycursor=db.cursor()
root=ttk.Toplevel()
root.geometry("1200x600")
root.title("safarcard")

def Add():
    print(bn.get())
    id=int(bn.get())
    route=br.get()

    sql="insert into safarcard.add_bus values(%d,'%s')"%(id,route)
    #value=(id,route)
    
    c=mycursor.execute(sql)
    print(c)
    db.commit()

    
    print((route.replace(' ','_')))
    route=route.replace(' ','_')
    sql="""
    CREATE TABLE `%s` (
  `stopname` varchar(45) DEFAULT NULL,
  `fare` int 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """%route
    c=mycursor.execute(sql)
    print(c)
    db.commit()
    #mycursor.close()

"""
    CREATE TABLE `add_bus` (
  `busno` int NOT NULL,
  `busroute` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`busno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
   
    
def Edit():
    id=int(bn.get())
    route=br.get()

    mycursor.execute("select  busroute from safarcard.add_bus where busno=%d"%id)
    records=mycursor.fetchall()
    print(records)
    sql="update safarcard.add_bus set busroute='%s' where busno=%d"%(route,id)
    c=mycursor.execute(sql)
    print(c)
    sql="ALTER TABLE safarcard.%s RENAME %s;"%(records[0][0],route)
    c=mycursor.execute(sql)
    print(c)
    db.commit()
    #mycursor.close()

def Delete():
    id=int(bn.get())
    
    route=br.get()

    sql="delete from safarcard.add_bus where busno=%d"%id
    c=mycursor.execute(sql)
    print(c)
    print(route)
    sql="drop table safarcard.%s"%route
    c=mycursor.execute(sql)
    print(c)
    db.commit()
    #mycursor.close()

def show():   
    
    mycursor.execute("select busno, busroute from safarcard.add_bus")
    records=mycursor.fetchall()
    print(records)

    for i, (busno,busroute) in enumerate(records,start=1):
        listbox.insert("","end",values=(busno,busroute))

    ttk.Button(root,text="Refresh",command=refresh,bootstyle="secondary").place(x=400,y=470)
    
    #listbox.delete(0-END)
column1=('Bus number','Bus route')
listbox=ttk.Treeview(root,columns=column1,show="headings")
for col in column1:
    listbox.heading(col,text=col)
    listbox.grid(row=2,column=0,columnspan=2)
    listbox.place(x=100,y=200)
def refresh():
    global listbox
    listbox.destroy()
    mycursor.execute("select busno, busroute from safarcard.add_bus")
    records=mycursor.fetchall()
    print(records)
    nlistbox=ttk.Treeview(root,columns=column1,show="headings")
    for col in column1:
        nlistbox.heading(col,text=col)
        nlistbox.grid(row=2,column=0,columnspan=2)
        nlistbox.place(x=100,y=200)
    for i, (busno,busroute) in enumerate(records,start=1):
        nlistbox.insert("","end",values=(busno,busroute))
    
    listbox=nlistbox
    
    

Label(root,text="Safar Card").grid(row=0,column=3)

busno=Label(root,text="Enter bus number").grid(row=2,column=2)
busroute=Label(root,text="Enter bus route").grid(row=4,column=2)
def combo():
    mycursor.execute("select busno from safarcard.add_bus")
    slist=mycursor.fetchall()
    values=[row[0] for row in slist]
    bn.configure(values=slist)
    db.commit()
bn=ttk.Combobox(root,postcommand=combo)
br=ttk.Entry(root)
bn.grid(row=2,column=3)
br.grid(row=6,column=3)
ttk.Button(root,text="Add",command=Add,bootstyle="primary").place(x=100,y=470)
ttk.Button(root,text="Edit",command=Edit,bootstyle="warning").place(x=200,y=470)
ttk.Button(root,text="Delete",command=Delete,bootstyle="danger").place(x=300,y=470)
ttk.Button(root,text="Show",command=show,bootstyle="info").place(x=400,y=470)


#ttk.Button(root,text="Refresh",command=refresh).place(x=400,y=430)

roo=Frame(root)
roo.place(x=550,y=100)

"""
Label(roo,text="Stop name").grid(row=1,column=2,sticky=E)
Label(roo,text="Fare").grid(row=1,column=3,sticky=E)
"""
def showsf():   
    table=listbox.selection()[0]
    a=listbox.item(table)['values'][1]
    a=a.replace(' ','_')
    sql="select stopname, fare from safarcard.%s"%a
    mycursor.execute(sql)
    records=mycursor.fetchall()
    print(records)

    for i, (stopname,fare) in enumerate(records,start=1):
        listboxe.insert("","end",values=(stopname,fare))

    ttk.Button(roo,text="Refresh",command=refreshsf,bootstyle="secondary").grid(row=3,column=2,sticky="ew")
    
    #listbox.delete(0-END)
"""
def refresh():
    listbox.destroy()
    mycursor.execute("select busno, busroute from safarcard.add_bus")
    records=mycursor.fetchall()
    print(records)
    nlistbox=ttk.Treeview(root,columns=column1,show="headings")
    for col in column1:
        nlistbox.heading(col,text=col)
        nlistbox.grid(row=2,column=0,columnspan=2)
        nlistbox.place(x=100,y=200)
    for i, (busno,busroute) in enumerate(records,start=1):
        nlistbox.insert("","end",values=(busno,busroute))

"""
column2=('Stopname','Fare')
nlistboxe=ttk.Treeview(roo,columns=column2,show="headings")
def refreshsf():
    global listboxe
    global listbox
    listboxe.destroy()
    print(listbox.selection())
    table=listbox.selection()[0]
    print(table)
    a=listbox.item(table)['values'][1]
    a=a.replace(' ','_')
    sql="select stopname, fare from safarcard.%s"%a
    mycursor.execute(sql)
    records=mycursor.fetchall()
    print(records)

    
    nlistboxe=ttk.Treeview(roo,columns=column2,show="headings")
    for col in column2:
        nlistboxe.heading(col,text=col)
        nlistboxe.grid(row=3,column=0,columnspan=2)
        #listbox.place(x=100,y=200)

    for i, (stopname,fare) in enumerate(records,start=1):
        nlistboxe.insert("","end",values=(stopname,fare))

    listboxe=nlistboxe

def addsf():
    stope=stops.get()
    faree=int(fare.get())
    table=listbox.selection()[0]
    a=listbox.item(table)['values'][1]
    a=a.replace(' ','_')
        #print(listbox.item(table)['values'][1])
    print(a)
    sql="insert into safarcard.%s values('%s', %d)"%(a,stope,faree)
    c=mycursor.execute(sql)
    print(c)
    db.commit()
    refreshsf()

def deletesf():
    
    table=listbox.selection()[0]
    a=listbox.item(table)['values'][1]
    a=a.replace(' ','_')
    t=listboxe.selection()[0]
    b=listboxe.item(t)['values'][0]
    print(a)
    print(b)
    
    sql="delete from safarcard.%s where stopname='%s'"%(a,b)
    c=mycursor.execute(sql)
    print(c)
    db.commit()
    refreshsf()

def editsf():
    table=listbox.selection()[0]
    a=listbox.item(table)['values'][1]
    a=a.replace(' ','_')
    try:
        t=listboxe.selection()[0]
        b=listboxe.item(t)['values'][0]
    except:
        t=nlistboxe.selection()[0]
        b=nlistboxe.item(t)['values'][0]
    print(a)
    print(b)

    stops.delete(0,END)
    stops.insert(0,b)
    thisbutt.grid(row=1,column=2,pady=10,padx=10)
    def delstop():
        faree=int(fare.get())
        print(a,b,faree)
        sql="update safarcard.%s set fare=%d where stopname='%s'"%(a,faree,b)
        c=mycursor.execute(sql)
        print(c)
        db.commit()
        refreshsf()
    thisbutt.config(command=delstop)
    #sql="update safarcard.%s set fare=%d where stopname=%s"%(a,faree,stop)
    #c=mycursor.execute(sql)
    #print(c)
    #db.commit()
ttk.Button(roo,text="Add",command=addsf,bootstyle="primary").grid(row=0,column=0,sticky="ew")
ttk.Button(roo,text="Edit",command=editsf,bootstyle="warning").grid(row=0,column=1,sticky="ew")
ttk.Button(roo,text="Delete",command=deletesf,bootstyle="danger").grid(row=0,column=2,sticky="ew")
ttk.Button(roo,text="Show",command=showsf,bootstyle="info").grid(row=3,column=2,sticky="ew")
stops=ttk.Entry(roo,textvariable="Stop name")
stops.grid(row=1,column=0,sticky=E,pady=10,padx=10)
fare=ttk.Entry(roo,text="Fare")
fare.grid(row=1,column=1,pady=10,padx=10)
stops.insert(0, "Enter Stopname")
fare.insert(0, "Enter Fare")


listboxe=ttk.Treeview(roo,columns=column2,show="headings")
for col in column2:
    listboxe.heading(col,text=col)
    listboxe.grid(row=3,column=0,columnspan=2)
    #listbox.place(x=100,y=200)

def stopstb():
    n=int(stops.get())
    thisbutt["state"]="disabled"
    stop=[]
    fare=[]
    for i in range(0,n):
        stop.append('')
        fare.append(None)
        stop[i]=ttk.Entry(roo,text="Enter stopname %d"%i)        
        fare[i]=ttk.Entry(roo,text="Enter fare %d"%i)
        
        stop[i].grid(row=i+2,column=1,pady=10,padx=10)
        fare[i].grid(row=i+2,column=2,pady=10,padx=10)
        fare[i].insert(0,"Fare")
        stop[i].insert(0,"Enter stopname")
    print(i)
    
    def ins():  
        for i in range(0,n):
            print(stop[i].get())
            print(fare[i].get())
            stope=stop[i].get()
            faree=int(fare[i].get())
            print(stope,faree)
            table=listbox.selection()[0]
            a=listbox.item(table)['values'][1]
            a=a.replace(' ','_')
            #print(listbox.item(table)['values'][1])
            print(a)
            sql="insert into safarcard.%s values('%s', %d)"%(a,stope,faree)
            c=mycursor.execute(sql)
            print(c)
            db.commit()
            """
             sql="insert into safarcard.add_bus values(%d,'%s')"%(id,route)
            #value=(id,route)
    
            c=mycursor.execute(sql)
            print(c)
            db.commit()
            """
            
            
    #ttk.Button(roo,text="Done",command=ins).grid(row=i+3,column=2,pady=10,padx=10)
      
thisbutt=ttk.Button(roo,text="Done",command=" ")

root.mainloop()