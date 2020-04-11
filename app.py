from flask import url_for,render_template,redirect,Flask,flash, session, request
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement, sqlerror   #Imported the mysqlconnect.py file from Make_tables folder

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='c828b6ff21f45063fd7860e5c1b1d233'

@app.route('/')
def home():
    flash("Yes")
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


# API to turn a normal user into an admin
# Send the data in JSON Format
# data = {
#   "userID": "b19188"
# }
@app.route("/makeadmin", methods=['POST'])
def make_admin():

    #Get the data
    data = request.get_json()
    uid = data['userID']
    #print(uid)

    #First check if session is actually logged in
    isLogin = False
    try:
        isLogin = session['logged_in']
    except KeyError as err:   #So that error will not come if the session is not defined
        return 'Error came: Key Error: '+str(err)

    if isLogin == True:

        #Now check if the loggined user is admin or not
        isadmin=session['admin']
        if(isadmin):
            # Now if it is an admin, check if the user exists
            try:
                stmt = "select admin from Users where userID='"+uid+"';"
                mycursor.execute(stmt)
                result = mycursor.fetchone()

                try:
                    #Checking if uid is already an Admin
                    if result[0] == 1:
                        return 'User Already an Admin!'
                    else:
                        #Changing the database
                        stmt = "UPDATE Users set admin=1 where userID='"+uid+"';"
                        mycursor.execute(stmt)
                        mydb.commit()
                        return 'Successfully made the user an admin'
                except:
                    #Certainly the result is empty, so user does not exist
                    return 'userID does not exists!'

            except sqlerror as err:
                return str(err)  #If some kind of sql error comes
        else:
            error = "Error, You are not an admin!"
            return error
    else:
        error = "You are not logged in, Please Login!"
        return 'error'  #API : Login should be ready after that we can use 
        #return render_template('login.html')

#API to turn an admin into a normal user
# Send the data in JSON Format
# data = {
#   "userID": "b19188"
# }
@app.route("/removeadmin", methods=['POST'])
def remove_admin(uid):

    #Get the data
    data = request.get_json()
    uid = data['userID']
    #print(uid)

    #First check if session is actually logged in
    isLogin = False
    try:
        isLogin = session['logged_in']
    except KeyError as err:   #So that error will not come if the session is not defined
        return 'Error came: Key_Error: '+str(err)

    if isLogin == True:     

        #Now check if the loggined user is admin or not
        isadmin = session['admin']
        if(isadmin):
        	# Now if it is an admin, check if the admin exists
            try:
                stmt = "select admin from Users where userID='"+uid+"';"
                mycursor.execute(stmt)
                result = mycursor.fetchone()

                try:
                    #Checking if uid is already an Admin
                    if result[0] == 1:
                        #Changing the database
                        stmt = "UPDATE Users set admin=0 where userID='"+uid+"';"
                        mycursor.execute(stmt)
                        mydb.commit()
                        return 'Successfully removed the admin'
                    else:
                        return 'User is already not an Admin!'
                except:
                    #Certainly the result is empty, so user does not exist
                    return 'userID does not exists!'

            except sqlerror as err:
                return str(err)  #If some kind of sql error comes
        else:
            error = "Error, You are not an admin!"
            return error
    else:
        error = "You are not logged in, Please Login!"
        return 'error'  #API : Login should be ready after that we can use 
        #return render_template('login.html')



if __name__=="__main__":
    app.run(debug=True)
