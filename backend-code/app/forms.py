from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, SelectField, TextAreaField, HiddenField, DateTimeField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email, AnyOf

def password_check(form, field):
    upperCase = False
    lowerCase = False
    
    for char in field.data:
        if(char.isupper):
            upperCase = True
        if(char.islower):
            lowerCase = True
    if(not upperCase or not lowerCase):
        raise ValidationError('Password must contain atleast 1 uppercase and 1 lowercase character')




class Sign_up_form(FlaskForm):
    name = StringField('Name:', [InputRequired(), Length(max=80)])
    email = EmailField('Email:', [InputRequired(), Email(message='Invalid Email')])
    password = PasswordField('Password:', [InputRequired(), Length(min=8, message='Password should be atleast 8 characters long')])
    confirm_password = PasswordField('Confirm Password:', [InputRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class Login_form(FlaskForm):
    email = EmailField('Email:', [InputRequired(), Email(message='Invalid Email')])
    password = PasswordField('Password:', [InputRequired()])
    submit = SubmitField('Login')


class Create_tracker_form(FlaskForm):
    name = StringField('Name:', [InputRequired()])
    tracker_type = SelectField('Tracker Type:', choices = [('Boolean', 'Boolean'), ('Numerical', 'Numerical'), ('Multiple Choice', 'Multiple Choice') ,('Time Duration', 'Time Duration')])
    description = TextAreaField('Description:')
    tracker_settings = HiddenField('Settings:')
    submit = SubmitField('Create Tracker')

class Create_log_form(FlaskForm):
    value = StringField('Value:', [InputRequired()])
    note = TextAreaField('Note:')
    timestamp = HiddenField('Timestamp:')
    submit = SubmitField('Add Log')
    