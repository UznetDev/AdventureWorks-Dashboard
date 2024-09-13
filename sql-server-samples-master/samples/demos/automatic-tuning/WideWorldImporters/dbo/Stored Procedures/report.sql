CREATE PROCEDURE [dbo].[report]
	@packagetypeid int
AS
BEGIN
    SELECT AVG([UnitPrice] * [Quantity] - [TaxRate])
    FROM [Sales].[OrderLines]
    WHERE [PackageTypeID] = @packagetypeid;
END;
GO