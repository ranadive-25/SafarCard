import mysql.connector as mysql

db=mysql.connect(host="cloud.googiehost.com",user="safarcar_sahil",password="sahil",database="safarcar_typ")
mycursor=db.cursor()
print(db)
