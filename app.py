from flask import url_for,render_template,redirect,Flask,flash,jsonify,request
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement   #Imported the mysqlconnect.py file from Make_tables folder
import datetime

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

@app.route("/add_event",methods=['POST']) #add a new event
def create_event():
	data=request.get_json()
	eventName=data["eventName"]
	about=data["about"]
	eventDate=data["eventDate"]
	eventTime=data["eventTime"]
	eventVenue=data["eventVenue"]
	clubID=data["clubID"]
	registered=data["registered"]
	attended=data["attended"]
	try:
		mycursor.execute("INSERT INTO Events(eventName, about, eventDate, eventTime, eventVenue, clubID, registered, attended) VALUES('"+eventName+"','"+about+"','"+eventDate+"','"+eventTime+"','"+eventVenue+"','"+clubID+"','"+registered+"','"+attended+"')")
		mydb.commit()
		return "Event added successfully!"
	except:
		return "Check the clubID."	
		


if __name__=="__main__":
    app.run(debug=True)
