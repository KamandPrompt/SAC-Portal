import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error as myerror

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
except myerror as err:
        print("Database sac_data does not exists")
        print() 


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

def get_tables_list(database='sac_data'):  #Defualt database sac_data, so no need to pass the data if not required
        existingTables = []
        mycursor.execute("use "+database+";")
        mycursor.execute("show tables;")
        for x in mycursor.fetchall():
                existingTables.append(x[0])
        return existingTables
