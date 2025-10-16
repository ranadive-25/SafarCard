import tkinter as tk 
from tkinter import *
import mysql.connector as mysql
from tkinter import messagebox
import ttkbootstrap
#connect to mysql workbench 
db=mysql.connect(host="localhost",user="root",password="5877",database="safarcard")
mycursor=db.cursor()

def register():
    #root.destroy()
    
    root.withdraw()
    ro=Toplevel(root)
    ro.title("Register")
    ro.geometry("2700x1900")
    ro.config()
    def back():
        ro.withdraw()
        root.deiconify()
    ttk.Button(ro,text="Back",command=back).grid(row=0, column=0,sticky=W)
    
    ttk.Label(ro,text="Register Here!!",font=("Times New Roman",30)).grid(row=0,column=1,padx=20,pady=20)
     
    r=Frame(ro) 
    r.grid(row=1,column=0,sticky=W) 
    
    ri=Frame(ro,width=500,height=500)
    ri.grid(row=1,column=2)
         
    img_label = tk.Label(ri)
    img_label.image = tk.PhotoImage(file="WhatsApp Image 2023-04-04 at 13.06.45.png")
    img_label['image'] = img_label.image
    img_label.pack(side = RIGHT, fill = Y)


    ttk.Label(r,text="Name").grid(row=1,column=0,padx=20,pady=20)  
    ttk.Label(r,text="Employee ID").grid(row=2,column=0,padx=20,pady=20)
    ttk.Label(r,text="Phone number").grid(row=3,column=0,padx=20,pady=20)
    ttk.Label(r,text="E-Mail ID").grid(row=4,column=0,padx=20,pady=20)
    ttk.Label(r,text="Role").grid(row=5,column=0,padx=20,pady=20)
    ttk.Label(r,text="Enter password").grid(row=7,column=0,padx=20,pady=20)
    ttk.Label(r,text="Re-enter password").grid(row=8,column=0,padx=20,pady=20)
    
    name=ttk.Entry(r)
    eid=ttk.Entry(r)
    phno=ttk.Entry(r)
    email=ttk.Entry(r)
    def sel():
        selection=str(var.get())
        print("You chose ",selection,type(selection))
        print(int(var.get()),type(int(var.get())))
    var=IntVar()
    admin=ttk.Radiobutton(r,text="Admin",variable=var,value=1,command=sel)
    cce=ttk.Radiobutton(r,text="Card Centre Employee",variable=var,value=2,command=sel)
    password=ttk.Entry(r)
    repassword=ttk.Entry(r)
    name.grid(row=1,column=1)
    eid.grid(row=2,column=1)
    phno.grid(row=3,column=1)
    email.grid(row=4,column=1)
    admin.grid(row=5,column=1,sticky=W)
    cce.grid(row=6,column=1,sticky=W)
    password.grid(row=7,column=1)
    repassword.grid(row=8,column=1)
    #if (int(var.get())==int(1)):
    
    def sub_admin():
        namee=name.get()
        eide=int(eid.get())
        phnoe=phno.get()
        emaile=email.get()
        passworde=password.get()
        if(len(namee)>44):
            messagebox.showerror("Error" , "Name should be less than 45 characters", parent = r)
        elif(len(phnoe)>10):
            messagebox.showerror("Error" , "Enter a valid phone number", parent = r)        
        else:
            print(namee,eide,phnoe,emaile,passworde)
            sql="insert into safarcard.admin values('%s',%d,'%s','%s','%s')"%(namee,eide,phnoe,emaile,passworde)
            c=mycursor.execute(sql)
            print(c)
            db.commit()
            ro.destroy()
            root.destroy()

    def sub_cce():
        namee=name.get()
        eide=int(eid.get())
        phnoe=phno.get()
        emaile=email.get()
        passworde=password.get()
        print(namee,eide,phnoe,emaile,passworde)
        sql="insert into safarcard.cce values('%s',%d,'%s','%s','%s')"%(namee,eide,phnoe,emaile,passworde)
        c=mycursor.execute(sql)
        print(c)
        db.commit()
        ro.destroy()
        root.destroy()


    def decide():
        if (int(var.get())==int(1)):
            sub_admin()
        elif(int(var.get())==int(2)):
            sub_cce()
        else:
            pass
    #elif(int(var.get())==int(2)):
    #    ttk.Button(r,text="Submit",command="",height=1,width=10,font=("Times New Roman",14,"bold")).grid(row=9, column=1,pady=40)
    #else:
    ttk.Button(r,text="Submit",command=decide).grid(row=9, column=1,pady=40)
    
    r.mainloop()

def login_as_admin():
    root.withdraw()
    global ttk
    r=ttk.Toplevel()
    #root.destroy()
    def admindashbmain():
        r.withdraw()
        import check
    r.title("Login")
    r.geometry("600x400")
    
    def back():
        r.withdraw()
        root.wm_deiconify()
    ttk.Button(r,text="Back",command=back).grid(row=0, column=0,sticky=W)
    
    Label(r,text="Login Here!!",font=("Times New Roman",30)).grid(row=0,column=1,padx=20,pady=20)
    ttk.Label(r,text="Employee ID").grid(row=1,column=0,padx=20,pady=20)
    ttk.Label(r,text="Enter password").grid(row=2,column=0,padx=20,pady=20)
    eid=ttk.Entry(r)
    password=ttk.Entry(r)
    eid.grid(row=1,column=1)
    password.grid(row=2,column=1)
    def admindashb():
        eide=int(eid.get())
        passwd=password.get()

        mycursor.execute("select * from admin where empid=%d and password = '%s'"%(eide,passwd))
        row = mycursor.fetchone()
        if row==None:
            messagebox.showerror("Error" , "Invalid Employee ID And Password", parent = r)
        else:
            messagebox.showinfo("Success" , "Successfully Login" , parent = r)
            admindashbmain()
			
    ttk.Button(r,text="Submit",command=admindashb,bootstyle="success").grid(row=3, column=1,pady=40)
    
  
    
def login_as_cce():
    root.withdraw()
    r=ttk.Toplevel()
    r.title("Login")
    r.geometry("600x400")
    r.config()
    def back():
        r.withdraw()
        root.deiconify()
    Button(r,text="Back",command=back).grid(row=0, column=0,sticky=NW)
    
    def ccedashbmain():
        r.withdraw()
        cc=ttk.Toplevel()
        cc.title("safarcard")
        cc.geometry("2700x1900")
        cc.config()
        def back():
            cc.withdraw()
            r.deiconify()
        ttk.Button(cc,text="Back",command=back).grid(row=0, column=0,sticky=NW)
    
        def add():
            frame=Frame(cc,width=1500,height=800)
            frame.grid(row=1,column=0,sticky=NW,padx=20)
            Label(frame,text=" ").grid(row=0,column=0,sticky=W,pady=10)  
            Label(frame,text="Name").grid(row=1,column=0,sticky=W,pady=10)  
            Label(frame,text="safarcard number").grid(row=2,column=0,sticky=W,pady=10)
            Label(frame,text="Phone number").grid(row=3,column=0,sticky=W,pady=10)
            Label(frame,text="E-Mail ID").grid(row=4,column=0,sticky=W,pady=10)
            Label(frame,text="Aadhar number").grid(row=5,column=0,sticky=W,pady=10)
            Label(frame,text="safarcard Account Balance").grid(row=6,column=0,sticky=W,pady=10)
            
            name=Entry(frame)
            cardno=Entry(frame)
            phno=Entry(frame)
            eid=Entry(frame)
            adharno=Entry(frame)
            balance=Entry(frame)
            
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
                sql="insert into safarcard.user values('%s',%d,'%s','%s','%s',%d)"%(namee,cardnoe,phnoe,emaile,adharnoe,balancee)
                c=mycursor.execute(sql)
                print(c)
                db.commit()
            ttk.Button(frame,text="Add",command=submituser,bootstyle="primary").grid(row=7, column=1,pady=40)
            

        def delete():
            fram=Frame(cc,width=1500,height=800)
            fram.grid(row=1,column=0,sticky=N)
            Label(fram,text="""
            """).grid(row=0,column=0)
            Label(fram,text="safarcard number ").grid(row=1,column=0)
            cardno=Entry(fram)
            cardno.grid(row=1,column=1)
            def deleteuser():
                cardnoe=int(cardno.get())

                sql="delete from safarcard.user where cardno=%d"%cardnoe
                c=mycursor.execute(sql)
                print(c)
                db.commit()
            ttk.Button(fram,text="Delete",command=deleteuser,bootstyle="danger").grid(row=2, column=1,pady=40)
            
            
        def update():
            frame=Frame(cc,width=1500,height=800)
            frame.grid(row=1,column=0,sticky=NE)
            Label(frame,text=" ").grid(row=0,column=0,sticky=W,pady=10)  
            Label(frame,text="Name").grid(row=1,column=0,sticky=W,pady=10)  
            Label(frame,text="safarcard number").grid(row=2,column=0,sticky=W,pady=10)
            Label(frame,text="Phone number").grid(row=3,column=0,sticky=W,pady=10)
            Label(frame,text="E-Mail ID").grid(row=4,column=0,sticky=W,pady=10)
            Label(frame,text="Aadhar number").grid(row=5,column=0,sticky=W,pady=10)
            Label(frame,text="safarcard Account Balance").grid(row=6,column=0,sticky=W,pady=10)
            name=Entry(frame)
            cardno=Entry(frame)
            phno=Entry(frame)
            eid=Entry(frame)
            adharno=Entry(frame)
            balance=Entry(frame)
            
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
                
                sql="update safarcard.user set name='%s',phno='%s',email='%s',adharno='%s',balance=%d where cardno=%d"%(namee,phnoe,emaile,adharnoe,balancee,cardnoe)
                c=mycursor.execute(sql)
                print(c)
                db.commit()
            ttk.Button(frame,text="Update",command=submituser,bootstyle="warning").grid(row=7, column=1,pady=40)
            

            
        cce=Frame(cc)
        cce.grid(row=0,column=0)

        Label(cce,text="safarcard",font=("Times New Roman",30)).grid(row=0,column=1,padx=20,pady=20)
        ttk.Button(cce,text="Add User",command=add,bootstyle="dark").grid(row=1, column=0,pady=40,sticky="ew")
        ttk.Button(cce,text="Delete User",command=delete,bootstyle="light").grid(row=1, column=1,pady=40,sticky="ew")
        ttk.Button(cce,text="Update User",command=update,bootstyle="dark").grid(row=1, column=2,pady=40,sticky="ew")
        frame=Frame(cc,width=1300,height=800)
        frame.grid(row=1,column=0,padx=20)
        add()
        delete()
        update()
        cce.mainloop()
        
        
    Label(r,text="Login Here!!",font=("Times New Roman",30)).grid(row=0,column=1,padx=20,pady=20)
    ttk.Label(r,text="Employee ID").grid(row=1,column=0,padx=20,pady=20)
    ttk.Label(r,text="Enter password").grid(row=2,column=0,padx=20,pady=20)
    eid=Entry(r)
    password=Entry(r)
    eid.grid(row=1,column=1)
    password.grid(row=2,column=1)
    def ccedashb():
        eide=int(eid.get())
        passwd=password.get()

        mycursor.execute("select * from cce where empid=%d and password = '%s'"%(eide,passwd))
        row = mycursor.fetchone()
        if row==None:
            messagebox.showerror("Error" , "Invalid Employee ID And Password", parent = r)
        else:
            messagebox.showinfo("Success" , "Successfully Login" , parent = r)
            ccedashbmain()
			
    ttk.Button(r,text="Submit",command=ccedashb,bootstyle="success").grid(row=3, column=1,pady=40)
  
ttk=ttkbootstrap 
root=ttk.Window(themename="morph")
root.title("safarcard")
root.config()
root.geometry("800x500")
ttk.Button(root,text="Register",command=register,bootstyle="info-outline").place(x=200,y=150)
ttk.Button(root,text="Login as Admin",command=lambda:login_as_admin()).place(x=150,y=250)
ttk.Button(root,text="Login as Card Centre Employee",command=login_as_cce).place(x=50,y=300)
     
img_label = ttk.Label(root)
img_label.image = tk.PhotoImage(file="WhatsApp Image 2023-04-04 at 13.06.45.png")
img_label['image'] = img_label.image
img_label.pack(side = RIGHT, fill = Y)


root.mainloop()
