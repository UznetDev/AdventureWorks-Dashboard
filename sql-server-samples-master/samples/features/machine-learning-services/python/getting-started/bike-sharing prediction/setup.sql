-- Before we start, we need to restore the database
-- Step1: Download the backup file (url)
--Save the file on a location where SQL Server can access it. For example: C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\Backup\

-- In a new query window in SSMS, execute the following restore statement, but REMEMBER TO CHANGE THE FILE PATHS
-- to match the directories of your installation!

USE master;
GO
RESTORE DATABASE velibDB
   FROM DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\Backup\velibDB.bak'
   WITH
                MOVE 'velibDB' TO 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\velibDB.mdf'
                ,MOVE 'velibDB_log' TO 'C:\Program Files\Microsoft SQL Server\MSSQL14.MSSQLSERVER\MSSQL\DATA\velibDB.ldf';
GO
