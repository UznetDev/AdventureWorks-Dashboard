set xact_abort on
go
begin distributed transaction
go
use dtclinux1
go
insert into dtctable values (1)
insert into dtc2.dtclinux2.dbo.dtctable values (1)
go
commit tran
go
