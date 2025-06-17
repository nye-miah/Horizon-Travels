import mysql.connector
from mysql.connector import errorcode


# MYSQL CONFIG VARIABLES
hostname = "localhost"
db = "horizontravels" #Optional
username = "root"
passwd = "ShitEater42!"
myport = "3306"

"""
# MYSQL CONFIG VARIABLES
hostname = "127.0.0.1"
db = "horizontravels" #Optional
username = "root"
passwd = "Shit_Eater42!"
myport = "3306"
"""
#The block of code below handles any errors with
# the database not working or the username and password
# being incorrect 
def getConnection():
    try:
        conn = mysql.connector.connect(host=hostname,
                                       port=myport,
                                       user=username,
                                       password=passwd,
                                       database=db) #database is optional
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or Password is not working")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:   #will execute if there is no exception raised in try block
        return conn


#Student Name: Nayeeb (Nye) Miah
#Student ID: 24018464
