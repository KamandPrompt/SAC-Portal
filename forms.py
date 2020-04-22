from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField, BooleanField

# I didn't use validators.Email() to validate email address since it is very primitive and needs furthur verification by other means such as email activation or lookups.

# userID is our roll no. 
#email is b1XXXX@students.iitmandi.ac.in

# Register Form Class
class RegisterForm(Form):
    userID = StringField('UserID', [validators.Length(6)])
    email = StringField('Email', [validators.Length(30)])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Confirm Password')
    name = StringField('Name', [validators.Length(min=1, max=30)])
    submit = SubmitField('Register')


#Login Form Class
class LoginForm(Form):
    userID = StringField('UserID', [validators.Length(6)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')
