from flask import Flask, flash, make_response, render_template, redirect, url_for, abort, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import gc
from functools import wraps
import mysql.connector
import dbfunc

app = Flask(__name__)
app.secret_key = 'my_secret_key' #key used for password hashing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
daba = SQLAlchemy(app)

#Route to Home Page
@app.route('/home')
@app.route('/index')
@app.route('/')
def index_override():
        conn = dbfunc.getConnection()
        if conn != None:
            print("MySQL Connection is established")
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT DISTINCT deptCity FROM routes;')
            #print('SELECT statement executed successfully.')
            rows = dbcursor.fetchall()
            dbcursor.close()
            conn.close()
            cities = []
            for city in rows:
                city = str(city).strip("(")
                city = str(city).strip(")")
                city = str(city).strip(",")
                city = str(city).strip("'")
                cities.append(city)
            return render_template('Horizon Travels.html', departureslist=cities)
        else:
            print('DB connection Error')
            return 'DB connection Error'
        #return render_template('Horizon Travels.html')


#Show admin/standard contents if usertype is admin/standard
@app.route('/index/<usertype>')
def index(usertype):
        conn = dbfunc.getConnection()
        if conn != None:
            print("MySQL Connection is established")
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT DISTINCT deptCity FROM routes;')
            #print('SELECT statement executed successfully.')
            rows = dbcursor.fetchall()
            dbcursor.close()
            conn.close()
            cities = []
            for city in rows:
                city = str(city).strip("(")
                city = str(city).strip(")")
                city = str(city).strip(",")
                city = str(city).strip("'")
                cities.append(city)
            return render_template('Horizon Travels.html', usertype=usertype, departureslist=cities)
        else:
            print('DB connection Error')
            return 'DB connection Error'
        #return render_template('Horizon Travels.html')
    #return render_template('Horizon Travels.html', usertype=usertype)

@app.route('/register', methods=['GET','POST'])
def register():
    error = ''
    print('Register start')
    try:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            if username and password and email:
                conn = dbfunc.getConnection()
                if conn != None:
                    if conn.is_connected():
                        print("MySQL Connection is established")
                        dbcursor = conn.cursor()
                        #Check if username/password exists already
                        password = sha256_crypt.hash((str(password)))
                        Verify_Query = "SELECT * FROM users WHERE username = %s;"
                        dbcursor.execute(Verify_Query,(username,))
                        rows = dbcursor.fetchall()
                        if dbcursor.rowcount > 0:
                            error = ("username already taken, please choose another")
                            return render_template("signup.html", error=error)
                        else: #This means we can add a new user
                            dbcursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (username, password, email))
                            conn.commit() #Saves data in database
                            print("Thanks for registering!")
                            dbcursor.close()
                            conn.close()
                            gc.collect()
                            #The three sessions below are the session variables
                            session['logged_in'] = True
                            session['username'] = username
                            session['usertype'] = 'standard' # by default, all users are standard
                            #return redirect(url_for("success_signup",\
                             #message='User registered successfully and logged in..'))
                            return render_template("success.html",\
                             message='User registered successfully and logged in..')
                    else:
                        print("Connection error1")
                        return 'DB Connection Error'
                else:
                    print("Connection error2")
                    return 'DB Connection Error'
            else:
                error = ('empty parameters')
                return render_template("signup.html", error=error)
        else:
            return render_template("signup.html", error=error)
    except Exception as e:
        error_message = str(e)
        if "1062" in error_message and "email" in error_message:
            error = "Email already registered, please use another."
        elif "1062" in error_message and "username" in error_message:
            error = "Username already taken, please choose another."
        else:
            error = "An unexpected error occurred. Please try again."
        print(f"Error during registration: {error_message}")

        return render_template("signup.html", error=error)
        #return render_template("signup.html", error=error)



@app.route('/login', methods=['GET','POST'])
def login():
    form ={}
    error = ''
    try:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            form = request.form
            print('login start 1.1')

            if username and password:
                conn = dbfunc.getConnection()
                if conn != None:
                    if conn.is_connected():
                        print('MySQL Connecion is established')
                        dbcursor = conn.cursor()
                        dbcursor.execute("SELECT password_hash, usertype \
                            FROM users WHERE username = %s;", (username,))
                        data = dbcursor.fetchone()
                        if dbcursor.rowcount < 1: #This means no user exists
                            error = "User / password does not exist. Try again"
                            return render_template("login.html", error=error)
                        else:
                            #verify password hash and password received from user
                            if sha256_crypt.verify(request.form['password'], str(data[0])):
                                session['logged_in'] = True
                                session['username'] = request.form['username']
                                session['usertype'] = str(data[1])
                                print("You are now logged in")
                                return render_template('userresources.html', 
                                                       message="Logged in successfully", \
                                    username=username, data="This is user specific data", \
                                        usertype=session['usertype'])
                            else:
                                error = "Incorrect username and/or password. Please try again."
                        gc.collect()
                        print('login start 1.10')
                        return render_template("login.html", form=form, error=error)
    except Exception as e:
        #error = "Invalid credentials, try again."
        error = f"An error occurred: {str(e)}"
        print (error)
        return render_template("login.html", error=error)
    return render_template("login.html", error=error)                



def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            print("You need to login first")
            return render_template('login.html', error="You need to login first")
    return wrap

@app.route("/logout")
@login_required
def logout():
    # Clear the session
    session.clear()
    print("You have been logged out")
    gc.collect()
    return render_template("Horizon Travels.html", optionalmessage="You have been logged out")

def standard_user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'standard'):
            return f(*args, ** kwargs)
        else:
            print("You need to login first as user")
            return render_template('login.html', error="You need to login first as user")
    return wrap 

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'admin'):
            return f(*args, ** kwargs)
        else:
            print("You need to login first as admin user")
            return render_template('login.html', error="You need to login first as admin user")
    return wrap  

@app.route('/userfeatures/')
@login_required
@standard_user_required
def user_features():
    print('fetchrecords')
    #records from database can be derived
    #user login can be checked
    print ("Welcome ", session['username'])
    return render_template('standarduser.html', \
        user=session['username'], message="User data from app and standard \ " \
        "user features can go here...")

@app.route('/adminfeatures/')
@login_required
@admin_required
def admin_features():
    print('create / amend records / delete reccords / generate reports')
    #Write business logic here
    #records from database can be derived
    #user login can be checked
    print ("Welcome ", session['username'])
    return render_template('adminuser.html', \
user=session['username'], message="User data from app and admin \ " \
        "user features can go here...")

@app.route('/generateadminreport/')
@login_required
@admin_required
def generate_admin_report():
    print("Admin reports")
    #Here you can generate required data as per business logic
    return """
    <h1> This is admin report for {} </h1>
    <a href='/adminfeatures')> Go to Admin Features page </a>
    """.format(session['username'])

@app.route('/generateuserrecord/')
@login_required
@standard_user_required
def generate_user_report():
    print("User records")
    #Here you can generate required data as per business logic
    return """
    <h1> This is User record for user {} </h1>
    <a href='/userfeatures')> Go to User Features page </a>
    """.format(session['username'])
                            
"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Retrieve user data from the database
        # Your database query code goes here

        # Check if username exists and password is correct
        if username and check_password_hash(username.password, password):
            session["user_id"] = username.id
            return redirect("/index")
        else:
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")


    """
"""
app.route('/cities_form')
def cities_form():
    conn = dbfunc.getConnection()
    if conn != None:
        print("MySQL Connection is established")
        dbcursor = conn.cursor()
        dbcursor.execute('SELECT DISTINCT deptCity FROM routes;')
        #print('SELECT statement executed successfully.')
        rows = dbcursor.fetchall()
        dbcursor.close()
        conn.close()
        cities = []
        for city in rows:
            city = str(city).strip("(")
            city = str(city).strip(")")
            city = str(city).strip(",")
            city = str(city).strip("'")
            cities.append(city)
        return render_template('citiesform.html', departurelist=cities)
    else:
        print('DB connection Error')
        return 'DB connection Error'
"""
    #if request.method == 'POST':
    #    if request.form['nm'] == 'nmiah' and request.form['pw'] == '123':
    #        return redirect(url_for('success'))
    #    else:
    #        abort(401)
    #else:
    #    return redirect(url_for('index'))

    
#@app.route ('/success/<name>')
#def success():
#    return ('logged in successfully')     
#    #flash('You were successfully logged in')

@app.route('/bookticket')
def bookticket():
    return render_template('booking_form.html')




@app.route ('/dumpVar', methods = ['POST', 'GET'])
def dumpVar():
    if request.method == 'POST':
        result = request.form

        output = "<H2>Data Received: </H2></br>"
        output += "Number of Data Fields : " + str(len(result))
        output += '<h3>Return to <a href = "/">Homepage</a></h3>'

        for key in list(result.keys()):
            output = output + " </br> " + result.get(key)
        return output

@app.route ('/selectBooking/', methods = ['POST', 'GET'])
def selectBooking():
    if request.method == 'POST':
        #print('Select booking initiated')
        departcity = request.form['departureslist']
        arrivalcity = request.form['arrivalslist']
        outdate = request.form['outdate']
        returndate = request.form['returndate']
        adultseats = request.form['adultseats']
        childseats = request.form['childseats']
        lookupdata = [departcity, arrivalcity, outdate, returndate, adultseats, childseats]
        print(lookupdata)
        conn = dbfunc.getConnection()
        if conn !=None:
            print('MySQL connection is established')
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT * FROM routes WHERE deptCity = %s AND arrivCity = %s;', (departcity, arrivalcity))
            print('SELECT statement executed.')
            rows = dbcursor.fetchall()
            datarows=[]
            for row in rows:
                data = list(row)
                fare = (float(row[5]) * float(adultseats)) + (float(row[5]) * 0.5 *float(childseats))
                print(fare)
                data.append(fare)
                print(data)
                datarows.append(data)
            dbcursor.close()
        conn.close()
        #print(datarows)
        #print(len(datarows))
        return render_template('booking_start.html', resultset=datarows, lookupdata=lookupdata)     

@app.route ('/booking_confirm/', methods = ['POST', 'GET'])
def booking_confirm():
    if request.method == 'POST':
        print('booking confirm initiated')
        journeyid = request.form['bookingchoice']
        departcity = request.form['deptcity']
        arrivalcity = request.form['arrivcity']
        outdate = request.form['outdate']
        returndate = request.form['returndate']
        adultseats = request.form['adultseats']
        childseats = request.form['childseats']
        totalfare = request.form['totalfare']
        cardnumber = request.form['cardnumber']

        totalseats = int(adultseats) + int(childseats)
        bookingdata = [journeyid, departcity, arrivalcity, outdate, returndate, adultseats, childseats, totalfare, cardnumber, totalseats]
        print(bookingdata)
        conn = dbfunc.getConnection()
        if conn != None:
            print("MySQL connection is established")
            dbcursor = conn.cursor()
            dbcursor.execute('INSERT INTO bookings (deptDate, arrivDate, idRoutes, noOfSeats, totFare) VALUES \
                (%s, %s, %s, %s, %s);', (outdate, returndate, journeyid, totalseats, totalfare))
            print('statement executed successfully.')
            conn.commit() # send info to database
            #dbcursor.execute('SELECT AUTO_INCREMENT - 1 FROM information_schema.TABLES)
            dbcursor.execute('SELECT LAST_INSERT_ID();')
            #print("SELECT statement executed successfully")
            rows = dbcursor.fetchone()
            #print ('row count: ' + str(dbcursor.rowcount))
            bookingid = rows[0]
            bookingdata.append(bookingid)
            dbcursor.execute('SELECT * FROM routes WHERE idRoutes = %s;', (journeyid,))
            rows = dbcursor.fetchall()
            deptTime = rows[0][2]
            arrivTime = rows[0][4]
            bookingdata.append(deptTime)
            bookingdata.append(arrivTime)
            print(bookingdata)
            print(len(bookingdata))
            cardnumber = cardnumber[-4:-1] #only shows the last 4 digits of the cardnumber
            print(cardnumber)
            dbcursor.execute
            dbcursor.close()
            conn.close() # connection must be closed
            return render_template('booking_confirm.html', resultset=bookingdata, cardnumber=cardnumber)
        else:
            print('DB connection Error')
            return redirect(url_for('index'))
        



# Flask's built-in error handler
app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

app.errorhandler(401)
def not_found_error(error):
    return render_template('401.html'), 401

if __name__ == '__main__':
    app.run(debug = True)

#Student Name: Nayeeb (Nye) Miah
#Student ID: 24018464
