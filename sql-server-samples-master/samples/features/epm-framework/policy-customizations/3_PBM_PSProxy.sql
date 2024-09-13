-- Create PS Proxy with valid credentials on SQL Server instances
CREATE CREDENTIAL [cred_PSProxy] WITH IDENTITY = N'User', SECRET = N'Pwd'
GO
USE [msdb]
GO
EXEC msdb.dbo.sp_add_proxy @proxy_name=N'Proxy_Powershell',@credential_name=N'cred_PSProxy', @enabled=1
GO
EXEC msdb.dbo.sp_grant_proxy_to_subsystem @proxy_name=N'Proxy_Powershell', @subsystem_id=12
GO
EXEC msdb.dbo.sp_grant_login_to_proxy @proxy_name=N'Proxy_Powershell', @msdb_role=N'SQLAgentUserRole'
GO