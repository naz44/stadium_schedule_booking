from flask import Flask, render_template, request, url_for, flash, redirect, session
import sqlite3, os
from werkzeug.exceptions import abort
from datetime import date
import datetime
import hashlib
#from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm, BookingForm, EditingForm, ChangePrices
from flask_mail import Mail, Message
from random import randint
from creds import email_password
app = Flask(__name__)
app.config['SECRET_KEY'] = 'stadium'

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='play.arena35@gmail.com'
app.config['MAIL_PASSWORD']=email_password #from settings change this before pushing to git
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

#connecting to database
def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/viewmaintenance')

def viewmaintenance():
    conn = get_db_connection()
    #displays all bookings in desc order of date
    filtered = conn.execute('SELECT * from maintenance').fetchall()
    conn.close()
    return render_template('viewmaintenance.html',data=filtered)

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
            user = conn.execute('SELECT * FROM users WHERE emailid = ? and password= ?',(e,str(hashlib.md5(p.encode()).hexdigest()))).fetchone()
            sports = conn.execute('SELECT * FROM sports').fetchall()
            conn.close()
            if user is None:
                #abort(404)
                flash("Invalid credentials",category="danger")
                return render_template('login.html',form=form)
            session['user']=e
            session['username'] = user['username']
        except:
            flash("Couldnot establish connection with the database, please try after sometime",category='warning')
            return render_template('index.html')
        else:
            if user['admin'] == 'yes':
                return redirect(url_for('adminhomepage'))
            #there are no favsports for admin
            favs = user['favsports']
            print(favs)
            favsports = [ i.strip().capitalize() for i in favs.split(',')]
            print(favsports)
            session['favsports']=favsports
            print(session['favsports'])
            sp_limit = {'Football': 14, 'Cricket': 14, 'Hockey': 12, 'Rugby': 15, 'Basketball': 10, 'Tennis': 4,
                            'Badminton': 4,
                            'Archery': 4, 'Golf': 6}
        return render_template('userhome.html', sports=sports, favsports=favsports, sp_limit=sp_limit)

    return render_template('login.html',form=form)


@app.route('/userhome')
def userhome():
    conn= get_db_connection()
    sports=conn.execute('select * from sports').fetchall()
    favsports=session['favsports']
    conn.close()
    sp_limit = {'Football': 14, 'Cricket': 14, 'Hockey': 12, 'Rugby': 15, 'Basketball': 10, 'Tennis': 4, 'Badminton': 4,
                'Archery': 4, 'Golf': 6}
    return render_template('userhome.html', sports=sports, favsports=favsports, sp_limit=sp_limit)

@app.route('/updatebooking', methods=('GET', 'POST'))
def updatebooking():
    sp = request.form.get('sp')
    dt = request.form.get('dt')
    tc = request.form.get('tc')
    hc = request.form.get('hc')
    sp_name = request.form.get('sp_name')
    slotlist = request.form.getlist('slotlist[]')
    code = ",".join(slotlist)
    print("HERE")
    print(session['user'])
    msg = Message(subject='Booking Cofirmed!', sender='play.arena35@gmail.com', recipients=[session['user']])
    msg.body = str(f"Your booking is confirmed.\nSport: {sp_name}\nTime: {code}\nTotal Cost: {tc}")
    msg.html = render_template('confirmation.html', dt=dt, slotlist=slotlist, hc=hc, tc=tc, sp=sp, sp_name=sp_name,
                               cnf=False)
    mail.send(msg)

    conn = get_db_connection()
    conn.execute("INSERT INTO booking (sportsId,date,duration,'total cost','customer username',code) VALUES (?,?,?,?,?,?)",(sp,dt,len(slotlist),tc,session['username'],code))
    conn.commit()
    conn.close()
    return ("nothing")

@app.route('/logout', methods=('GET', 'POST'))
def logout():
    #check user login 
    if "user" in session:
        flash("Logged out successfully",category='success')
        session.clear()
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
            conn.execute("INSERT INTO users (username,emailid,password,firstname,lastname,favsports,admin) VALUES (?,?,?,?,?,?,?)",(un,e,str(hashlib.md5(p.encode()).hexdigest()),fn,ln,fs,'no'))
            sports = conn.execute('SELECT * FROM sports').fetchall()
            flash("Thank you for registering",category='success')
            favsports = [i.strip().capitalize() for i in fs.split(',')]
            conn.commit()
            conn.close()
        except:
            flash("Couldnot add your details to the database, please try after sometime",category='warning')
            #display error accordingly---
        else:
            return redirect(url_for("login"))

    return render_template('register.html',form=form)

@app.route('/forgotpassword', methods=('GET', 'POST'))
def forgotpassword():
    #get email from dbase 
    #and send reset password otp to user via mail
    #validate otp 
    #and redirect to reset password,update in dbase
    form=ForgotPasswordForm()
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
            session['email']=e
            #print(session['otp'])
            msg=Message(subject='OTP',sender='play.arena35@gmail.com',recipients=[e])
            msg.body=str(otp)
            mail.send(msg)
            return render_template('verify.html')

    return render_template('forgotpassword.html',form=form)

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if int(session['otp'])==int(user_otp):
        session.pop('otp',None)
        return redirect(url_for('resetpassword'))
    return render_template('verify.html' , string ="Enter the correct OTP")

@app.route('/resetpassword',methods=['GET','POST'])
def resetpassword():
    form=ResetPasswordForm()
    if form.is_submitted():
        result= request.form 
        try:
            conn = get_db_connection()
            password = request.form.get('password')
            confirmPassword = request.form.get('password_confirm')
            if confirmPassword == password and password != "":
                #update the table 
                conn.execute('UPDATE users SET password = ? WHERE emailid = ?',(str(hashlib.md5(password.encode()).hexdigest()),session['email']))
            elif password == "" and confirmPassword == "":
                return render_template('resetpassword.html',form =form, message = "Need to give a password")
            else:
                return render_template('resetpassword.html',form =form, message = "Passwords donot match")
            conn.commit()
            conn.close()
        except:
            flash("Couldnot update the database, recheck your details and try after sometime",category='warning')
        else:
            flash('Password reset done successfully.',category='success')
            session.pop('email',None)
            return redirect(url_for('login'))

    return render_template('resetpassword.html',form=form)

@app.route('/bookinghistory')
def bookinghistory():
    conn = get_db_connection()
    #displays all bookings in desc order of date
    filtered = conn.execute('SELECT b."customer username",s.name,b.date,b.duration,b."total cost" FROM booking b,sports s where b.sportsid=s.id order by b.date desc').fetchall()
    conn.close()
    return render_template('bookinghistory.html',data=filtered)

@app.route('/adminhomepage')
def adminhomepage(): 
    return render_template('adminhomepage.html')

@app.route('/homepage')
def homepage(): 
    conn= get_db_connection()
    sports=conn.execute('select * from sports').fetchall()
    favsports=session['favsports']
    conn.close()
    return render_template('homepage.html', sports=sports, favsports=favsports)

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
        cur_date_bookings_maintenance = conn.execute('SELECT code FROM maintenance WHERE sportsid = (SELECT id from sports WHERE name = ?) and date = ?', (sport, datestr)).fetchall()
        booking_list = []
        for booking in cur_date_bookings:
            booking_list.extend([j.strip() for j in booking['code'].split(',')])
        for booking in cur_date_bookings_maintenance:
            booking_list.extend([j.strip() for j in booking['code'].split(',')])
        availability[datestr] = booking_list
    sp = sport
    sportsdata = conn.execute('SELECT * FROM sports WHERE name = ?',(sp,)).fetchone()
    session['sport_id']=sportsdata['id']
    conn.close()
    return render_template('book.html', sport=sport, dates=dates, availability=availability, sportsdata=sportsdata, form=form)

@app.route('/confirmbooking', methods=('GET', 'POST'))
def confirmbooking():
    form=BookingForm()
    if request.method == "POST" and form.is_submitted():
        result= request.form
        dt = request.form.get('date')
        slotlist = request.form.getlist('slot_list[]')
        hc = request.form.get('cost-per-hr')
        tc = request.form.get('form-total-cost')
        sp = request.form.get('sport-id')
        sp_name = request.form.get('sport-name')
        return render_template('confirmation.html', form=form, dt=dt, slotlist=slotlist, hc=hc, tc=tc, sp=sp, sp_name=sp_name,cnf=True)
    return render_template('login.html', form=LoginForm())


@app.route('/editsports', methods=('GET', 'POST'))
def editsports():
    conn = get_db_connection()
    sports = conn.execute("select * from sports").fetchall()
    # print(sports)
    conn.close()
    sp_limit = {'Football': 14, 'Cricket': 14, 'Hockey': 12, 'Rugby': 15, 'Basketball': 10, 'Tennis': 4,
                'Badminton': 4,
                'Archery': 4, 'Golf': 6}
    return render_template('editsports.html', sports=sports, sp_limit=sp_limit)
    

@app.route('/edit', methods=('GET', 'POST'))
def edit():
    form = EditingForm()
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
        cur_date_bookings_maintenance = conn.execute('SELECT code FROM maintenance WHERE sportsid = (SELECT id from sports WHERE name = ?) and date = ?', (sport, datestr)).fetchall()
        booking_list = []
        for booking in cur_date_bookings:
            booking_list.extend([j.strip() for j in booking['code'].split(',')])
        availability[datestr] = booking_list
        for booking in cur_date_bookings_maintenance:
            booking_list.extend([j.strip() for j in booking['code'].split(',')])
    sp = sport

    sportsdata = conn.execute('SELECT * FROM sports WHERE name = ?',(sp,)).fetchone()
    session['edit_id']= sportsdata['id']
    # print(session['edit_id'])
    # print(type(session['edit_id']))
    conn.close()
    return render_template('edit.html', sport=sport, dates=dates, availability=availability, sportsdata=sportsdata, form=form)


@app.route('/maintenance', methods=('GET', 'POST'))
def maintenance():
    form=EditingForm()
    if request.method == "POST" and form.is_submitted():
        print("HEREE")
        result= request.form
        conn = get_db_connection()
        p = request.form.get('date')
        # print(p)
        slotlist = request.form.getlist('slot_list[]')
        # print(slotlist)
        s = request.form.get('sport-id')
        # print(type(s))
        # print(type(','.join(slotlist)))
        comment_maintenance=request.form.get('comment')
        conn.execute('INSERT INTO maintenance (sportsId,date,duration,comment,customer_username,code) values (?,?,?,?,?,?)',(int(session['edit_id']),p,len(slotlist),comment_maintenance,'admin',','.join(slotlist)))
        # conn.execute('INSERT INTO booking (sportsId,date,duration,total_cost,customer_username,code) values (?,?,?,?,?,?)',(int(session['edit_id']),p,len(slotlist),0,'admin',','.join(slotlist)))
        session.pop('edit_id',None)
        conn.commit()
        conn.close()
        flash("Details have been updated",category='success')
        return render_template('adminhomepage.html', form=form, p=p)
    return render_template('login.html', form=LoginForm())

@app.route('/changeprices', methods=['GET','POST'])
def changeprices():
    # fetches all the sports from sports table and displays on changeprices.html. After submit, it updates the the price.
    form = ChangePrices()
    if form.is_submitted():
        sport = request.form.get('sports')
        price = request.form.get('price')
        conn=get_db_connection()
        conn.execute('UPDATE sports SET cost = ? WHERE name = ?', (int(price),sport))
        conn.commit()
        conn.close()
        flash("Price has been updated", category='success')
        return redirect(url_for('adminhomepage'))
    conn=get_db_connection()
    query = conn.execute('select name from sports').fetchall()
    conn.commit()
    conn.close()
    print(query)
    return render_template("changeprices.html",query=query, form = form)

if __name__ == "__main__":
    app.run(debug=True)