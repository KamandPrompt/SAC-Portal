from flask import url_for,render_template,redirect,Flask,flash, session, request, jsonify
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement, sqlerror   #Imported the mysqlconnect.py file from Make_tables folder

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

# API To add a club
# Example of JSON Data to be sent
# data = {
#    "clubID": "C10001",
#    "clubName": "Programming club"
#    "about": "About of the club upto 600 Characters"
#    "type": "open"/"close"    What type of club it is? open or close
# }
@app.route("/addclub", methods=['POST'])
def add_club():
    # First check if the user is logged in or not
    isLogin = False
    try:
        isLogin = session["logged_in"]
    except KeyError as err:
        return "Error KeyError: "+str(err)
    
    if(isLogin):
        # Now check if user is an admin
        isAdmin = session['admin']

        if(isAdmin):
            # Now get the user data in JSON Form
            data = request.get_json()

            # Create the insert statment
            data['tablename']="Clubs"
            stmt = create_insert_statement(data)  # It will automatically create the insert statement
            # Example:
            # INSERT INTO Clubs(clubID,clubName,about,type) VALUES('C10001','PC','About','open');
            #print(stmt)

            # Executing mysql statements
            success = 0; msg=''
            try:
                mycursor.execute(stmt)
                mydb.commit()
                msg = "Added CLub Successfully"
                success=1
                return jsonify(success=success, msg=msg)
            except sqlerror:
                msg = "Error: "+str(sqlerror)
                return jsonify(success=success, msg=msg)
                
        else:
            error = "Access Denied! You are not an admin"
            return error
    else:
        error = "Not Logined! Please Login First"
        return error




if __name__=="__main__":
    app.run(debug=True)
