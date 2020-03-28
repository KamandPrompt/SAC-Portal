from mysqlconnect import mydb

mycursor = mydb.cursor()
mycursor.execute("use sac_data")
mycursor.execute("show tables")
tables = mycursor.fetchall()
for i in tables:
	print("Table Name:",i[0])
	mycursor.execute("describe "+i[0])
	desription = mycursor.fetchall()
	for j in desription:
		print(*j)
	print()