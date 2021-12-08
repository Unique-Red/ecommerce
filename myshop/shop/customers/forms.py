from wtforms import Form, StringField, PasswordField, validators
from wtforms.fields.simple import SubmitField

class CustomerRegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])  
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    country = StringField('Country', [validators.DataRequired()])
    state = StringField('State', [validators.DataRequired()])
    city = StringField('City', [validators.DataRequired()])
    contact = StringField('Contact', [validators.DataRequired()])
    address = StringField('Address', [validators.DataRequired()])

    submit = SubmitField("Register")

class CustomerLoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email()])
    password = PasswordField('New Password', [validators.DataRequired()])
