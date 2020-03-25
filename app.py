import flask
from forms import LoginForm
app=flask.Flask(__name__)
app.config['SECRET_KEY']='c828b6ff21f45063fd7860e5c1b1d233'

@app.route('/')
def home():
    return flask.render_template('basic.html')

@app.route("/login",methods=['GET','POST'])
def Login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data[1:6].isdecimal() and form.email.data[6:]=='@students.iitmandi.ac.in' :
            flask.flash('You have logged-in successfully','success')
            return flask.redirect(flask.url_for('home'))
        else:
            flask.flash('Invalid Email/Password','danger')
    return flask.render_template('login.html',form=form)

if __name__=="__main__":
    app.run(debug=True)
