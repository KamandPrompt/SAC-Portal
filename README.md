# SAC-Portal
SAC Portal for IIT Mandi

This is a project to build a portal for the Student Activity Center of IIT Mandi . This portal will be used by clubs to post details about their events which will be read by students who have enrolled for that particular club. This website is being built with flask web application framework .

Forking and Cloning
---
To get started with the project , go ahead and fork the repository . You should see the URL change to
```
https://github.com/Your Username/SAC-Portal
```
To clone this repository , copy the URL. Open your terminal or git bash and enter the following aftering replacing your username. 
```
git clone https://github.com/Your Username/SAC-Portal.git
```

Running the app
---

It is recommended to work in virtual environments and here we will be working in python3 , then install the required dependencies using
```
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

Then to run the app,
```
python3 app.py
```

Creating Database
---

We are using the mysql server as our database
So, ensure to install mysql server and configure it

Now to create the database on your local machine,
First add the following details in '.env' file here:
```
DATABASE_HOST=localhost
DATABASE_PORT=3306
#Default Host is localhost with Port: 3306
DATABASE_USER=your-username
DATABASE_PASSWORD=your-password
```

Then, go to Make_Tables folder,
Then run the file 'createdatabase.py' after setting this
```
python3 createdatabase.py
```

The database with the tables will be created. If error comes, check that you have entered correct details for your database in .env file and mysql is running in your computer.




