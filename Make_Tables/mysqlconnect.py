import mysql.connector
import os
from dotenv import load_dotenv

directory = os.getcwd()
envindex = directory.find('Make_Tables')
if envindex!=-1:  #If current working directory is Make_Tables
	load_dotenv(directory[:envindex]+"/.env")
else:
	load_dotenv(directory+"/.env")

mydb = mysql.connector.connect(
        host = os.environ.get("DATABASE_HOST"),
        user = os.environ.get("DATABASE_USER"),
        password = os.environ.get("DATABASE_PASSWORD"),
        port = os.environ.get("DATABASE_PORT")
	)
mycursor = mydb.cursor()
try:
        mycursor.execute("use sac_data;")
except:
        print("sac_data does not exists")


def create_insert_statement(data):   #pass the data in the JSON Format
        
        
        '''   #Column names should be the keys
        data = {   
                "tablename" : 'Users',
                "userid" : 'B19188',
                "email" : 'b19188@students.iitmandi.ac.in',
                "password" : 'Priyam@0911',
                "name" : 'Priyam Seth',
                "admin" : '1'
        } 
        '''
        clst=""+data["tablename"]+"("
        vlst="("
        data.pop("tablename")
        for key in data:
                clst+=key+","
                vlst+="'"+data[key]+"',"

        if clst[-1]==',':
                clst=clst[:-1]
        if vlst[-1]==',':
                vlst=vlst[:-1]
        clst+=")"
        vlst+=')'

        stmt = "INSERT INTO "+clst+" VALUES"+vlst+";"
        return stmt
