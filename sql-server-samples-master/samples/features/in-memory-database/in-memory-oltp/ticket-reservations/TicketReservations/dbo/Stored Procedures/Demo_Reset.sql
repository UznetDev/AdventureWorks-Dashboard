
create proc Demo_Reset
as
DECLARE @isMemoryTable BIT

SELECT @isMemoryTable = is_memory_optimized FROM sys.tables
WHERE [name] = 'TicketReservationDetail'

IF(@isMemoryTable= 1) DELETE dbo.TicketReservationDetail
ELSE TRUNCATE TABLE dbo.TicketReservationDetail;

