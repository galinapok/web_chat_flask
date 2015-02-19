from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, PasswordField, validators,  SelectField
from wtforms.validators import Email, Required
from flask.ext.wtf.file import FileField

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat')
    photo = FileField('Your photo')
    accept_tos = SelectField(u'Gender',coerce=str, choices=[('male','Male'), ('female','Female')])
   
class loginForm(Form):
    user= TextField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class RegisterRoomForm(Form):	
    room_name= TextField('Room name', [validators.Length(min=4, max=25), validators.Regexp('^\w+$', flags=0, message="Room name should contain only [a-zA-Z0-9_] symbols")])
   