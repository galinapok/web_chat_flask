from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators
from wtforms.validators import Email, Required
from flask.ext.wtf.file import FileField

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    photo = FileField('Your photo')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

class loginForm(Form):
    user= TextField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])

class RegisterRoomForm(Form):	
    room_name= TextField('Room name', [validators.Length(min=4, max=25)])
   