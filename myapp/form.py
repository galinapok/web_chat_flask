from flask.ext.wtforms import Form
from wtforms import TextField, PasswordField, Required, Email
from wtforms.validators import ValidationError

from app.models import User

class EmailPasswordForm(Form):
    email = TextField('Email', validators=[Required(), Email(),
        Unique(
            User,
            User.email,
            message='There is already an account with that email.')])
    password = PasswordField('Password', validators=[Required()])

class Unique(object):
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

from flask_wtf.file import FileField

class PhotoForm(Form):
    photo = FileField('Your photo')
