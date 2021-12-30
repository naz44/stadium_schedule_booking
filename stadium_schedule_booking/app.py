from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3, os
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'stadium'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')

def get_db_connection():
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=('GET', 'POST'))
def login():
    #get details from login page and validate
    #according to the user(admin/customer) display the homepage
    return render_template('login.html')

@app.route('/home', methods=('GET', 'POST'))
def userhome():
    conn = get_db_connection()
    # cursor = conn.cursor()
    # sports = cursor.execute("SELECT * FROM sports")
    sports = conn.execute('SELECT * FROM sports').fetchall()
    imgurls = []
    for sp in sports:
        url = "< img src = \"{{url_for('static', filename='images/"+sp[1]+".jpg')}}\" class =\"card-img-top\" alt=\"card image X-UA-Compatible\">"
        imgurls.append(url)
    conn.close()

    return render_template('userhome.html', sports=sports, imgurls=imgurls)

if __name__ == "__main__":
    app.run(debug=True)

