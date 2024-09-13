@echo off
 set pwd=Passwd__%random%
echo Building the SQL Linux Docker container
docker pull mcr.microsoft.com/mssql/server:2017-latest
docker build -t sqllinux prep
echo Running the SQL linux docker image
start cmd /k docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=%pwd%" -e "MSSQL_SA_PASSWORD=%pwd%" -h sqlserver --name sqlserver  -p:1433:1433 --rm sqllinux
echo Waiting 90 seconds for SQL server to restore WideWorldImporters
timeout /t 90
setlocal
echo running tests against SQL 2017 database WideWorldImporters
set TEST_PASSWORD=%pwd%
dotnet publish src -o out
dotnet vstest src\out\SmoSamples.dll /logger:console /settings:src\localhost.runsettings
endlocal
echo Terminating docker container
docker kill sqlserver
