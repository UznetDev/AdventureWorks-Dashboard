-- Before we start, we need to restore the DB for this tutorial.
-- Step1: Download the compressed backup file (https://deve2e.azureedge.net/sqlchoice/static/TutorialDB.bak)
--Save the file on a location where SQL Server can access it. For example: C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Backup\
-- In a new query window in SSMS, execute the following restore statement, but REMEMBER TO CHANGE THE FILE PATHS
-- to match the directories of your installation!
USE master;
GO
RESTORE DATABASE TutorialDB
   FROM DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\Backup\TutorialDB.bak'
   WITH
                MOVE 'TutorialDB' TO 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\TutorialDB.mdf'
                ,MOVE 'TutorialDB_log' TO 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\TutorialDB.ldf';
GO
