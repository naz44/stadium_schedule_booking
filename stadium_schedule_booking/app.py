from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from forms import LoginForm, SignupForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stadium'

@app.route('/')
def index():
    return render_template('index.html')

#connecting to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
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
        conn.close()
        if user is None:
            #abort(404)
            return "Invalid creds"
        return render_template('homepage.html')

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
        flash("Thank you for registering")
        conn.commit()
        conn.close()
        return render_template('homepage.html')

    return render_template('register.html', form=form)

@app.route('/forgotpassword', methods=('GET', 'POST'))
def forgotpassword():
    #get email from dbase 
    # and send reset password link to user via mail
    
    return render_template('forgotpassword.html')
