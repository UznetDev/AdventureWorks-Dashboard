USE [Clinic]
GO

ALTER TABLE [dbo].[Patients]
ALTER COLUMN [SSN] [char](11) COLLATE Latin1_General_BIN2
WITH (ONLINE = ON)
GO

ALTER TABLE [dbo].[Patients]
ALTER COLUMN [LastName] [nvarchar](50) COLLATE Latin1_General_BIN2
WITH (ONLINE = ON)
GO

ALTER TABLE [dbo].[Patients]
ALTER COLUMN [BirthDate] [datetime2](7)
WITH (ONLINE = ON)
GO

DBCC FREEPROCCACHE
GO
