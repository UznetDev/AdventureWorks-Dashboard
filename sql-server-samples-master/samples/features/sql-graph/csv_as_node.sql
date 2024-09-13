/*
Bulk insert a csv file using bcp
*/

-- CREATE TABLE
DROP TABLE IF EXISTS Graph.Customers;

CREATE TABLE Graph.Customers(
	CustomerID int,
	CustomerName nvarchar(100) not null,
	BillToCustomerID int not null,
	CustomerCategoryID int not null,
	BuyingGroupID int null,
	PrimaryContactPersonID int not null,
	AlternateContactPersonID int null,
	DeliveryMethodID int not null,
	DeliveryCityID int not null,
	PostalCityID int not null,
	CreditLimit decimal(18, 2) null,
	AccountOpenedDate date not null,
	StandardDiscountPercentage decimal(18, 3) not null,
	IsStatementSent bit not null,
	IsOnCreditHold bit not null,
	PaymentDays int not null,
	PhoneNumber nvarchar(20) not null,
	FaxNumber nvarchar(20) null,
	DeliveryRun nvarchar(5) null,
	RunPosition nvarchar(5) null,
	WebsiteURL nvarchar(256) not null,
	DeliveryAddressLine1 nvarchar(60) not null,
	DeliveryAddressLine2 nvarchar(60) null,
	DeliveryPostalCode nvarchar(10) not null,
	DeliveryLocation geography null,
	PostalAddressLine1 nvarchar(60) not null,
	PostalAddressLine2 nvarchar(60) null,
	PostalPostalCode nvarchar(10) not null,
	LastEditedBy int not null,
	ValidFrom datetime2(7) not null,
	ValidTo datetime2(7) not null
) AS NODE;
go

-- to improve performance, disable default indexes
ALTER INDEX ALL ON Graph.Customers disable;
go

/* SQL Server only
-- to improve performance, set the recovery mode to bulk_logged
USE master;
go

ALTER DATABASE [WideWorldImporters-Standard]
SET recovery bulk_logged;
go
*/

/*
:: From a windows command line, run the following commands.
:: The first line retrieves [WideWorldImporters-Standard].[Sales].[Customers] as a csv file.
bcp [WideWorldImporters-Standard].[Sales].[Customers] out "E:\Graph Examples\Graph.Customers.csv" -w -U {userName}@{serverName} -S tcp:{serverName}.database.windows.net -P {password}
::
:: The second line inserts a column $node_id into the csv file
python csv_as_node.py -f "E:\\Graph Examples\\Graph.Customers.csv" -s "Graph" -t "Customers"
::
:: The third and last line inserts the newly created csv file "E:\Graph Examples\Graph.Customers_as_node.csv" into [WideWorldImporters-Standard].[Graph].[Customers]
bcp [WideWorldImporters-Standard].[Graph].[Customers] in "E:\Graph Examples\Graph.Customers_as_node.csv" -w -U {userName}@{serverName} -S tcp:{serverName}.database.windows.net -P {password}
*/

/* SQL Server only
ALTER DATABASE [WideWorldImporters-Standard]
SET recovery full;
go

USE [WideWorldImporters-Standard];
go
*/

ALTER INDEX ALL ON Graph.Customers rebuild;
go

select * from Graph.Customers;
go
