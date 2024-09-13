import pyodbc
server = 'myserver'
database = 'mydb'
username = 'myusername'
password = 'mypassword'

#Connection String
connection = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()

#Sample select query
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print row[0]
    row = cursor.fetchone()

