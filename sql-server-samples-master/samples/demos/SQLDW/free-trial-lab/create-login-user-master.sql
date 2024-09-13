-- Connect to master database and create a login
CREATE LOGIN XLRCLogin WITH PASSWORD = ' a123reallySTRONGpassword!';
CREATE USER XLRCUser FOR LOGIN XLRCLogin;
