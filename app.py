from flask import url_for,render_template,redirect,Flask,flash, session
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

#API to turn a normal user into an admin
@app.route("/makeadmin/<uid>", methods=['POST'])
def make_admin(uid):
    #First check if session is actually logged in

    if session['logged_in'] == True:

        #Now check if the loggined user is admin or not
        isadmin=0
        try:
            stmt = "select admin from Users where userID='"+session['username']+"';"
            mycursor.execute(stmt)
            isadmin = int(mycursor.fetchone()[0])
        except sqlerror as err:
            return str(err)

        # Now if it is an admin, check if the user exists
        if(isadmin):
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
        return render_template('login.html', error = error)  #API : Login should be ready

#API to turn an admin into a normal user
@app.route("/removeadmin/<uid>", methods=['POST'])
def remove_admin(uid):
    #First check if session is actually logged in

    if session['logged_in'] == True:

        #Now check if the loggined user is admin or not
        isadmin=0
        try:
            stmt = "select admin from Users where userID='"+session['username']+"';"
            mycursor.execute(stmt)
            isadmin = int(mycursor.fetchone()[0])
        except sqlerror as err:
            return str(err)

        # Now if it is an admin, check if the admin exists
        if(isadmin):
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
        return render_template('login.html', error = error)  #API : Login should be ready



if __name__=="__main__":
    app.run(debug=True)
