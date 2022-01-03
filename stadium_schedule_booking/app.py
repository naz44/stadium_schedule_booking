from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3, os
from werkzeug.exceptions import abort
from forms import LoginForm, SignupForm, BookingForm
from datetime import date
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'stadium'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
        # connection = sqlite3.connect('database.db')
        # cur = connection.cursor()
        conn = get_db_connection()
        p = request.form.get('password')
        e = request.form.get('email')
        user = conn.execute('SELECT * FROM users WHERE emailid = ? and password = ?',(e,p)).fetchone()
        sports = conn.execute('SELECT * FROM sports').fetchall()
        conn.close()
        if user is None:
            #abort(404)
            return "Invalid creds"
        favs = user['favsports']
        print(favs)
        favsports = [ i.strip().capitalize() for i in favs.split(',')]
        print(favsports)
        return render_template('userhome.html', sports=sports, favsports=favsports)

    return render_template('login.html', form=form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    #get details from register page 
    # and insert into database
    form=SignupForm()
    if form.is_submitted():
        result= request.form 
        # connection = sqlite3.connect('database.db')
        # cur = connection.cursor()
        conn = get_db_connection()
        p = request.form.get('password')
        e = request.form.get('email')
        fn= request.form.get('firstname')
        ln= request.form.get('lastname')
        fs= request.form.get('favsports')
        un= request.form.get('username')
        conn.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",(un,e,p,fn,ln,fs,'no'))
        sports = conn.execute('SELECT * FROM sports').fetchall()
        flash("Thank you for registering")
        favsports = [i.strip().capitalize() for i in fs.split(',')]
        conn.commit()
        conn.close()
        return render_template('userhome.html', sports=sports, favsports=favsports) # Cricke, Football

    return render_template('register.html', form=form)

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
    #get email from dbase 
    # and send reset password link to user via mail
    
    return render_template('forgotpassword.html')

if __name__ == "__main__":
    app.run(debug=True)