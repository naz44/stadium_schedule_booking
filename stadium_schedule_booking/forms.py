from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import email_validator
class LoginForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired("Please enter your email address."), validators.Email("This field requires a valid email address")])
    password = PasswordField('Password',[validators.InputRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username=StringField('Username', [validators.InputRequired()])
    firstname=StringField('firstname', [validators.InputRequired()])
    lastname=StringField('lastname', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired("Please enter your email address."), validators.Email("This field requires a valid email address")])
    favsports=StringField('favsports', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Sign up')

class BookingForm(FlaskForm):
    submit = SubmitField('Proceed')
    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired("Please enter your email address."), validators.Email("This field requires a valid email address")])
    submit = SubmitField('Send password reset email')

