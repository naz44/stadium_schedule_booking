from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(),validators.Length(min=6, max=35)])
    password = PasswordField('Password',[validators.DataRequired(),validators.Length(min=6, max=15)])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username=StringField('Username', [validators.DataRequired(),validators.Length(min=4, max=25)])
    firstname=StringField('firstname', [validators.DataRequired(),validators.Length(min=1, max=35)])
    lastname=StringField('lastname', [validators.DataRequired(),validators.Length(min=1, max=35)])
    email = StringField('Email', [validators.DataRequired(),validators.Length(min=6, max=35)])
    favsports=StringField('favsports', [validators.DataRequired(),validators.Length(min=6, max=35)])
    password = PasswordField('Password', [validators.DataRequired(),validators.Length(min=6, max=15)])
    submit = SubmitField('Sign up')

class BookingForm(FlaskForm):
    submit = SubmitField('Proceed')