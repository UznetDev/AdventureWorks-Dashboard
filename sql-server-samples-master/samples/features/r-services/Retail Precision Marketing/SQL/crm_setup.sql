use sqlr;
go
drop table if exists CDNOW;
go

-- create the fraud table to hold invoice data:

create table CDNOW(
	[ID] int not null,
	[Date] date not null,
	[Volume] int not null,
	[Amount] float not null);
go

-- Modify path to the data file: "CDNOW_master.csv"

bulk insert CDNOW
from 'C:\sqlr\mydemos\CRM\CDNOW_master.csv'
with(
	fieldterminator = ',',
	firstrow = 2);
go

--create clustered columnstore index cs_CDNOW on CDNOW;
--go

grant select on CDNOW to rdemo;
go
