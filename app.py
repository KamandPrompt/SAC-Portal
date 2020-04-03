from flask import url_for,render_template,redirect,Flask,flash, request, jsonify, session
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement, sqlerror   #Imported the mysqlconnect.py file from Make_tables folder
#use sqlerror to track errors in mysql databases

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


@app.route('/leaveclub', methods = ['POST'])
def leave_club():
    ''' Example of JSON data to be send
    data = {
        "clubID" : "C10001"
        }
    '''
    is_login = session['logged_in']
    #is_login = True

    if(is_login):
        data = request.get_json()
        usrID = session['username']
        stmt = "DELETE FROM ClubMembers WHERE userID='"+userID+"' and clubID='"+data["clubID"]+"';"
        #print(stmt)
        success = 0;msg=''
        try:
            mycursor.execute(stmt)
            mydb.commit()
            success=1
            msg = "Deleted"
        except sqlerror as err:
            success=0
            msg = str(err)
        
        return(jsonify(success=success,msg=msg))
    else:
        error = "Not logged in, Please Log In!"
        #This will only work if login.html is defined
        return render_template('login.html', error = error, form =form)

if __name__=="__main__":
    app.run(debug=True)
