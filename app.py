from flask import url_for,render_template,redirect,Flask,flash,session
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement   #Imported the mysqlconnect.py file from Make_tables folder

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='c828b6ff21f45063fd7860e5c1b1d233'

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login",methods=['GET','POST'])
def Login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data[1:6].isdecimal() and form.email.data[6:]=='@students.iitmandi.ac.in' :
            flash('You have logged-in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Invalid Email/Password')
    return render_template('login.html',title='Login | SAC Portal, IIT Mandi',form=form)

@app.route("/AddCoordinator",methods=['POST'])
def AddCoordinator():
    email=session['email'][0:6]
    isadmin=mycursor.execute('SELECT EXISTS(SELECT * from Coordinators WHERE userID="'+email+'");')
    if(isadmin):
        userID=request.args['userID']
        clubID=request.args['clubID']
        try:
            mycursor.execute('INSERT into Coordinators VALUES("'+clubID+'","'+userID+'");')
            mydb.commit()
            return 'Data inserted successfully'
        except:
            return 'Error Inserting Data'

    else:
        return 'Sorry! You are not an Admin'

if __name__=="__main__":
    app.run(debug=True)

