pwd=Pwd$RANDOM
echo Building the SQL Linux Docker container
docker pull mcr.microsoft.com/mssql/server:2017-latest
docker build -t sqllinux prep
echo Running the SQL linux docker image
docker run -e ACCEPT_EULA=Y -e SA_PASSWORD=$pwd -e MSSQL_SA_PASSWORD=$pwd -h sqlserver --name sqlserver  -p:1433:1433 -d --rm sqllinux
echo Waiting 2 minutes for SQL server to restore WideWorldImporters
sleep 120
echo running tests against SQL 2017 database WideWorldImporters
export TEST_PASSWORD=$pwd
dotnet publish src
dotnet vstest src/bin/Debug/netcoreapp2.1/SmoSamples.dll --logger:console --Settings:src/localhost.runsettings
echo Terminating docker container
docker kill sqlserver
