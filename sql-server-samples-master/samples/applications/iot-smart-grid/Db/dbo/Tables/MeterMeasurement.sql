CREATE TABLE [dbo].[MeterMeasurement] (
    [MeasurementID]    BIGINT         IDENTITY (1, 1) NOT NULL,
    [MeterID]          INT            NOT NULL,
    [MeasurementInkWh] DECIMAL (9, 4) NOT NULL,
    [PostalCode]       NVARCHAR (10)  NOT NULL,
    [MeasurementDate]  DATETIME2 (7)  NOT NULL,
    PRIMARY KEY NONCLUSTERED HASH ([MeasurementID]) WITH (BUCKET_COUNT = 16777216),
    INDEX [ix] NONCLUSTERED HASH ([MeterID]) WITH (BUCKET_COUNT = 1048576)
)
WITH (DURABILITY = SCHEMA_ONLY, MEMORY_OPTIMIZED = ON);

