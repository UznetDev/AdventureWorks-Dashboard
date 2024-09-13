-- CTAS statement to create Trip table with hashed distribution on DateID column
CREATE TABLE dbo.TripHashed
WITH
(
DISTRIBUTION = Hash(DateID),
CLUSTERED COLUMNSTORE INDEX
)
AS SELECT * FROM dbo.Trip;
