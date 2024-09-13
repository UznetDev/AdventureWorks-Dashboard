-- Creates statistics on the Date and Trip DateID columns to check join performance improvements
CREATE STATISTICS [dbo.Date DateID stats] ON dbo.Date (DateID);
CREATE STATISTICS [dbo.Trip DateID stats] ON dbo.Trip (DateID);
