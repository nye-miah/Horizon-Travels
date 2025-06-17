import mysql.connector

try:
    db = mysql.connector.connect(
        host='localhost',
        user="root",
        passwd="ShitEater42!"
    )
    print("connection sucessful")
except Exception as e:
    print("not connected")


#Student Name: Nayeeb (Nye) Miah
#Student ID: 24018464
