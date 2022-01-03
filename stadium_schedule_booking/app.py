from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3, os
from werkzeug.exceptions import abort
#from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm, BookingForm, ResetPasswordForm
from datetime import date
import datetime
from flask_mail import Mail, Message
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stadium'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='spyjason123@gmail.com'
app.config['MAIL_PASSWORD']='' #from settings change this before pushing to git                   
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

#connecting to database
def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/login', methods=('GET', 'POST'))
def login():
    #get details from login page and validate
    #according to the user(admin/customer) display the homepage
    form=LoginForm()
    if form.is_submitted():
        result= request.form 
        try:
            conn = get_db_connection()
            p = request.form.get('password')
            e = request.form.get('email')
            user = conn.execute('SELECT * FROM users WHERE emailid = ? and password= ?',(e,p)).fetchone()
            sports = conn.execute('SELECT * FROM sports').fetchall()
            #check= check_password_hash(user['password'],p)
            conn.close()
            if user is None:
                #abort(404)
                flash("Invalid credentials",category='error')
                return render_template('login.html',form=form)
            session['user']=e
            favs = user['favsports']
            print(favs)
            favsports = [ i.strip().capitalize() for i in favs.split(',')]
            print(favsports)
            
        except:
            flash("Couldnot establish connection with the database, please try after sometime",category='warning')

            return render_template('index.html')
        else:
            if user['admin'] == 'yes':
                    return render_template('adminhomepage.html')
        return render_template('userhome.html', sports=sports, favsports=favsports)

    return render_template('login.html',form=form)

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    #check user login 
    if "user" in session:
        session.pop('user', None)
        flash("Logged out successfully",category='success')
        return render_template('index.html')
    
    flash("User not logged in, please login first",category='warning')
    #return render_template('login.html',form=LoginForm())#error
    return redirect(url_for("login"))

@app.route('/register', methods=('GET', 'POST'))
def register():
    #get details from register page 
    # and insert into database
    form=SignupForm()
    if form.is_submitted():
        result= request.form 
        try:
            conn = get_db_connection()
            p = request.form.get('password')
            e = request.form.get('email')
            fn= request.form.get('firstname')
            ln= request.form.get('lastname')
            fs= request.form.get('favsports')
            un= request.form.get('username')
            conn.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",(un,e,p,fn,ln,fs,'no'))
            sports = conn.execute('SELECT * FROM sports').fetchall()
            flash("Thank you for registering",category='success')
            favsports = [i.strip().capitalize() for i in fs.split(',')]
            conn.commit()
            conn.close()
        except:
            flash("Couldnot establish connection with the database, please try after sometime",category='warning')
            #display error accordingly---
        else:
            return redirect(url_for("login"))

    return render_template('register.html',form=form)

@app.route('/book', methods=('GET', 'POST'))
def book():
    form = BookingForm()
    sport = request.args.get('sport')
    print(sport)
    dates = [] # To store next 7 days
    availability = {}   # availability = {"31/12/21": [11,12,21], "01/01/22": [2,3,18,19]}
    today = date.today()
    conn = get_db_connection()

    for i in range(7):
        dt = today+datetime.timedelta(days=i)
        datestr = str(dt.strftime("%d/%m/%Y"))
        dates.append([datestr, dt.strftime("%A") if i>0 else "Today"])
        #print(datestr)
        cur_date_bookings = conn.execute('SELECT code FROM booking WHERE sportsid = (SELECT id from sports WHERE name = ?) and date = ?', (sport, datestr)).fetchall()
        booking_list = []
        for booking in cur_date_bookings:
            booking_list.extend([j.strip() for j in booking['code'].split(',')])
        availability[datestr] = booking_list
    sp = sport
    sportsdata = conn.execute('SELECT * FROM sports WHERE name = ?',(sp,)).fetchone()

    conn.close()
    return render_template('book.html', sport=sport, dates=dates, availability=availability, sportsdata=sportsdata, form=form)

@app.route('/confirmbooking', methods=('GET', 'POST'))
def confirmbooking():
    form=BookingForm()
    if request.method == "POST" and form.is_submitted():
        print("HEREE")
        result= request.form
        conn = get_db_connection()
        p = request.form.get('date')
        print(p)

        # conn.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",(un,e,p,fn,ln,fs,'no'))
        # sports = conn.execute('SELECT * FROM sports').fetchall()
        # flash("Thank you for registering")
        # favsports = [i.strip().capitalize() for i in fs.split(',')]
        # conn.commit()
        # conn.close()
        # return render_template('userhome.html', sports=sports, favsports=favsports)

        return render_template('confirmbooking.html', form=form, p=p)
    return render_template('login.html', form=LoginForm())


@app.route('/forgotpassword', methods=('GET', 'POST'))
def forgotpassword():
    #and send reset password otp to user via mail
    #validate otp 

    # and redirect to reset password,update in dbase---
    form=ResetPasswordForm()
    if form.is_submitted():
        result= request.form 
        try:
            conn = get_db_connection()
            e = request.form.get('email')
            user = conn.execute('SELECT * FROM users WHERE emailid = ?',(e, )).fetchone()
            conn.close()
            if user is None:
                #abort(404)
                flash("Please enter your registered email id only",category='warning')
                return render_template('forgotpassword.html',form=form)
        except:
            flash("Couldnot establish connection with the database, please try after sometime",category='warning')
        else:
            flash('A password reset email has been sent to your registered mail.',category='info')
            #email=request.form['email']
            otp=randint(000000,999999)
            session['otp']=otp
            #print(session['otp'])
            msg=Message(subject='OTP',sender='spyjason123@gmail.com',recipients=[e])
            msg.body=str(otp)
            mail.send(msg)
            return render_template('verify.html')

    return render_template('forgotpassword.html',form=form)

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if int(session['otp'])==int(user_otp):
        session.pop('otp',None)
        return "<h3>Email success</h3>"
    return render_template('verify.html' , string ="Enter the correct OTP")

@app.route('/bookinghistory')
def bookinghistory():
    return render_template('bookinghistory.html')#should be dynamic---

if __name__ == "__main__":
    app.run(debug=True)