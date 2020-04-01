from flask import url_for,render_template,redirect,Flask,flash,request
from forms import LoginForm
from Make_Tables.mysqlconnect import mydb, mycursor, create_insert_statement   #Imported the mysqlconnect.py file from Make_tables folder
import numpy as np

app=Flask(__name__,static_url_path='/public')
app.config['SECRET_KEY']='c828b6ff21f45063fd7860e5c1b1d233'
app.jinja_env.filters['zip'] = zip

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/login",methods=['GET','POST'])
def Login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data[1:6].isdecimal() and form.email.data[6:]=='@students.iitmandi.ac.in' :
            flash('You have logged-in successfully!',category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Invalid Email/Password',category='failure')
    return render_template('login.html',title='Login | SAC Portal, IIT Mandi',form=form)

@app.route('/<uid>/joinclub',methods=['GET','POST'])
def join(uid):
    mycursor.execute('SELECT name FROM users WHERE userID="{0}"'.format(uid))
    check=mycursor.fetchall()
    if not len(check):
        return("<title>404 Forbidden</title><h1>404 Forbidden : You don't have access to this page!</h1>")
    mycursor.execute("SELECT MemberRequests.requestMessage,clubs.clubName FROM MemberRequests INNER JOIN clubs WHERE MemberRequests.reqStatus='Accepted' AND MemberRequests.clubID=clubs.clubID AND MemberRequests.userID='{0}'".format(uid))
    mess=mycursor.fetchall()
    if len(mess):
        for i in mess:
            flash('Your request to '+i[0]+' '+i[1]+' has been approved!',category='success')
    mycursor.execute("SELECT MemberRequests.requestMessage,clubs.clubName FROM MemberRequests INNER JOIN clubs WHERE MemberRequests.reqStatus='Rejected' AND MemberRequests.clubID=clubs.clubID AND MemberRequests.userID='{0}'".format(uid))
    mess=mycursor.fetchall()
    if len(mess):
        for i in mess:
            flash('Your request to '+i[0]+' '+i[1]+' has been rejected!',category='failure')
    mycursor.execute('DELETE FROM MemberRequests WHERE reqStatus!="Pending" AND userID="{0}"'.format(uid))
    mydb.commit()

    mycursor.execute("SELECT clubName,type,clubID FROM clubs WHERE clubID NOT IN (SELECT clubID FROM clubmembers WHERE userID='{0}') AND clubID NOT IN (SELECT clubID FROM MemberRequests WHERE requestMessage='Join' AND userID='{0}'); ".format(uid))
    notjoined=np.array(mycursor.fetchall())
    mycursor.execute("SELECT clubName,type,clubID FROM clubs WHERE clubID IN (SELECT clubID FROM clubmembers WHERE userID='{0}') ; ".format(uid))
    joined=mycursor.fetchall()
    clubsnotjoined=[]
    clubsjoined=[]
    for i in range(len(notjoined)):
        clubsnotjoined.append(notjoined[i][0])
    for i in range(len(joined)):
        clubsjoined.append(joined[i][0])

    if request.method=='POST':
        data=request.form
        for club in data:
            i=clubsnotjoined.index(club)
            if notjoined[i][1]=={'open'}:
                    mycursor.execute("INSERT INTO clubmembers VALUES('{0}','{1}')".format(uid,notjoined[i][2]))
                    mydb.commit()
                    flash('You have successfully joined '+notjoined[i][0],category="success")
                    return redirect('/'+uid+'/joinclub')
            else:
                print('Inside',notjoined[i][0])
                mycursor.execute("INSERT INTO MemberRequests VALUES('{0}','{1}','{2}','Pending')".format(uid,'Join',notjoined[i][2]))
                mydb.commit()
                flash('Your request has been sent. It will be approved/dissaproved by the Club Coordinator',category="success")
                return redirect('/'+uid+'/joinclub')
    return render_template('joinclub.html',notjoined=clubsnotjoined,joined=clubsjoined,title='Join a Club! | SAC Portal')

@app.route('/<uid>/requests',methods=['GET','POST'])
def approve(uid):
    mycursor.execute("SELECT clubID FROM coordinators WHERE userID='{0}' ".format(uid))
    clubs=mycursor.fetchall()
    if request.method=='POST':
        user,clubid,status=list(request.form.to_dict().keys())[0].split()
        print('User : ',user)
        if status=='accept':
            mycursor.execute('INSERT INTO ClubMembers VALUES ("{0}","{1}")'.format(user,clubid))
            mycursor.execute('UPDATE MemberRequests SET reqStatus="Accepted" WHERE clubID="{0}" AND userID="{1}"; '.format(clubid,user))
            mydb.commit()
        else:
            mycursor.execute('UPDATE MemberRequests SET reqStatus="Rejected" WHERE clubID="{0}" AND userID="{1}";'.format(clubid,user))
            mydb.commit()
    if len(clubs):
        reqList=[]
        for i in clubs:
            mycursor.execute("SELECT MemberRequests.userID,MemberRequests.requestMessage,clubs.clubName,MemberRequests.clubID FROM MemberRequests INNER JOIN clubs WHERE MemberRequests.clubID='{0}' AND reqStatus='Pending' AND MemberRequests.clubID=clubs.clubID;".format(i[0]))
            reqList.extend(mycursor.fetchall())
        return render_template("approve.html",reqList=reqList,title='Approve Requests | SAC-Portal')
    else:
        return("<title>404 Forbidden</title><h1>404 Forbidden : You don't have access to this page!</h1>")

if __name__=="__main__":
    app.run(debug=True)
