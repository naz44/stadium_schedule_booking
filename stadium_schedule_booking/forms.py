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

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', [validators.InputRequired("Please enter your email address."), validators.Email("This field requires a valid email address")])
    submit = SubmitField('Send password reset email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[
        validators.InputRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField(label='Passwordconfirm', validators=[
        validators.InputRequired()
    ])
    submit = SubmitField('Submit')

class BookingForm(FlaskForm):
    submit = SubmitField('Proceed')

class EditingForm(FlaskForm):
    submit = SubmitField('Proceed')

class ChangePrices(FlaskForm):
    submit = SubmitField('Proceed')