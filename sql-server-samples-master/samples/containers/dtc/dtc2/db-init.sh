#wait for the SQL Server to come up
sleep 20s

echo "running set up script"
#run the setup script to create the DB and the schema in the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Sql2019isfast -d master -i db-init.sql
