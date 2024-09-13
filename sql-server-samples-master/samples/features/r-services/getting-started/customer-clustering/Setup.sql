-- Before we start, we need to restore the DB for this tutorial.
-- Step1: Download the compressed backup file
-- Save the file on a location where SQL Server can access it. For example: C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Backup\
-- In a new query window in SSMS, execute the following restore statement, but REMEMBER TO CHANGE THE FILE PATHS
-- to match the directories of your installation!
USE master;
GO
RESTORE DATABASE tpcxbb_1gb
   FROM DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Backup\tpcxbb_1gb.bak'
   WITH
                MOVE 'tpcxbb_1gb' TO 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\tpcxbb_1gb.mdf'
                ,MOVE 'tpcxbb_1gb_log' TO 'C:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\DATA\tpcxbb_1gb.ldf';
GO