from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from passlib.hash import sha256_crypt
from forms import RegisterForm, LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement   #Imported the mysqlconnect.py file from Make_tables folder
import gc
from helper import not_logged_in, is_logged_in


app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='c828b6ff21f45063fd7860e5c1b1d233'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


# Home page before logging in
@app.route('/')
def home():
    return 'Home page of SAC-Portal.'


# User Registration
@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():

    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        
        if (form.userID.data[0] == 'b' or form.userID.data[0] == 'd' or form.userID.data[0] == 't' or form.userID.data[0] == 's' or form.userID.data[0] == 'v' ) and form.userID.data[1:6].isdecimal :
            userID = form.userID.data
        else:
            return 'Not a valid userID!'

        if form.email.data[0:6] == form.userID.data and form.email.data[6:]=='@students.iitmandi.ac.in' :
            email = form.email.data
        else:
            return 'Please enter valid email!'
        name = form.name.data
        password = sha256_crypt.hash(str(form.password.data))
        admin = 0
        
        mycursor.execute("SELECT * FROM Users WHERE userID = (%s)", (userID,))

        row = mycursor.fetchone()

        if row != None:   #checking for duplicate Users(if User already registered, can't register again)
            return 'This User already exists!'
        else:

            # Execute query
            mycursor.execute("INSERT INTO Users(userID, email, password, name, admin) VALUES(%s, %s, %s, %s, %s)", (userID, email, password, name, admin))

            # Commit to DB
            mydb.commit()
        
            flash('You are now registered and can log in!', 'success')
            gc.collect()  #garbage collection for memory issues

            return redirect(url_for('login'))

    return jsonify(form.errors) 



# User login by filling userID and password fields (userID and password must be enough as our userID(roll no.) and email represent same content)

# A Login WTForm for logging in similar to RegisterForm


@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():

        # Get Form Fields
        userID = form.userID.data
        password_candidate = form.password.data

        # Get User by userID
        mycursor.execute("SELECT * FROM Users WHERE userID = %s", (userID,))


        # Get stored data from database
        row = mycursor.fetchone()   #data get stored in tuple
        if row == None:
            return 'userID not found!'
        else:
            password = row[2]    #hashed password from database
            email = row[1]
            admin = row[4]

        
        # Compare Passwords
        if sha256_crypt.verify(password_candidate, password):
            # Passed

            session['logged_in'] = True
            session['userID'] = userID
            session['email'] = email
            session['admin'] = admin

            flash('You are now logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            return 'Password is incorrect!'


    return jsonify(form.errors)


#Dashboard (page) after Logging in
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return 'Welcome to SAC-Portal!'

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out!', 'success')
    return redirect(url_for('home'))



if __name__=="__main__":
    app.run(debug=True)
