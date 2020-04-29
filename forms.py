from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SubmitField, BooleanField, ValidationError

# I didn't use validators.Email() to validate email address since it is very primitive and needs furthur verification by other means such as email activation or lookups.

# userID is our roll no. 
#email is b1XXXX@students.iitmandi.ac.in

# Register Form Class

def userID_check(form, field):
    u = form.userID.data
    l = ['b','d','t','s','v']
    if (len(u) != 6 or u[0] not in l or u[1:6].isdecimal == False) :
        raise ValidationError('Please enter valid userID!')

def email_check(form, field):
    e = form.email.data
    if (len(e) != 30 or e[0:6] != form.userID.data or e[6:] != '@students.iitmandi.ac.in') :
        raise ValidationError('Please enter valid email address!')

class RegisterForm(Form):
    userID = StringField('UserID', [userID_check])
    email = StringField('Email', [email_check])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match!')])
    confirm = PasswordField('Confirm Password')
    name = StringField('Name', [validators.Length(min=1, max=30)])
    submit = SubmitField('Register')


#Login Form Class
class LoginForm(Form):
    userID = StringField('UserID', [validators.Length(6)])
    password = PasswordField('Password', [validators.DataRequired()])
    submit = SubmitField('Login')
