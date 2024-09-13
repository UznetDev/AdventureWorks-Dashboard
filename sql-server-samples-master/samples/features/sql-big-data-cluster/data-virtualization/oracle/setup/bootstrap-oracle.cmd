@echo off
REM bootstrap sample oracle tables CMD script
setlocal enableextensions
set ORACLE_SERVER=%1
set ORACLE_USER=%2
set ORACLE_PASSWORD=%3

if NOT DEFINED ORACLE_SERVER goto :usage
if NOT DEFINED ORACLE_USER goto :usage
if NOT DEFINED ORACLE_PASSWORD goto :usage

for %%F in (sqlplus.exe sqlldr.exe) do (
    echo Verifying %%F is in path & CALL WHERE /Q %%F || GOTO exit
)


for %%F in (sales-user.sql inventory.sql customer.sql) do (
    echo Executing [%%F]...
    echo exit | sqlplus -S %ORACLE_USER%/%ORACLE_PASSWORD%@%ORACLE_SERVER% @%%F || GOTO exit
)

for %%F in (inventory.ctl customer.ctl) do (
    echo Loading [%%F]...
    sqlldr CONTROL=%%F userid=%ORACLE_USER%/%ORACLE_PASSWORD%@%ORACLE_SERVER% || GOTO exit
)

endlocal
exit /b 0
goto :eof

:exit
    echo Bootstrap of the sample tables failed.
    exit /b 1

:usage
    echo USAGE: %0 ^<ORACLE_SERVER^> ^<ORACLE_USER^> ^<ORACLE_PASSWORD^>
    exit /b 0