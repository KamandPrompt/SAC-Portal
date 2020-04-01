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

@app.route("/update_event/<clubID>/<eventID>") #update an existing event
def update_event(clubID,eventID):
	data=request.get_json()
	eventName=data["eventName"]
	about=data["about"]
	eventDate=data["eventDate"]
	eventTime=data["eventTime"]
	eventVenue=data["eventVenue"]
	registered=data["registered"]
	attended=data["attended"]
	query1="UPDATE Events SET eventName='"+eventName+"', about='"+about+"', eventDate='"+eventDate+"', eventTime='"+eventTime+"', eventVenue='"+eventVenue+"', registered='"+registered+"', attended='"+attended+"'  WHERE clubID ='"+clubID+ "'AND eventID='"+eventID+"'"
	try:
		mycursor.execute(query1)
		mydb.commit()
		return "Event updated successfully."
	except:
		return "Check the clubID and eventID."

@app.route("/del_event/<clubID>/<eventID>") #delete an event
def del_event(clubID,eventID):
	query="DELETE FROM Events WHERE clubID ='"+clubID+ "'AND eventID='"+eventID+"'"
	try:
		mycursor.execute(query)
		mydb.commit()
		return "Event deleted successfully."
	except:
		return "Check the clubID and eventID"
		
		


if __name__=="__main__":
    app.run(debug=True)
