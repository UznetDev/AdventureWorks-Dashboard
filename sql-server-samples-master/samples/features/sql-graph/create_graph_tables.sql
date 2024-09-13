-- clean database
DROP TABLE IF EXISTS Graph.Customers;
DROP TABLE IF EXISTS Graph.StockItems;
DROP TABLE IF EXISTS Graph.Suppliers;

DROP TABLE IF EXISTS Graph.OrderLines_CustomersToStockItems;
DROP TABLE IF EXISTS Graph.OrderLines_StockItemsToCustomers;

DROP TABLE IF EXISTS Graph.InvoiceLines_CustomersToStockItems;
DROP TABLE IF EXISTS Graph.InvoiceLines_StockItemsToCustomers;

DROP TABLE IF EXISTS Graph.PurchaseOrderLines_SuppliersToStockItems;
DROP TABLE IF EXISTS Graph.PurchaseOrderLines_StockItemsToSuppliers;

DROP SCHEMA IF EXISTS Graph;
go

-- define schema
CREATE SCHEMA Graph;
go

/* SALES schema */
-- create node table for Sales.Customers
CREATE TABLE Graph.Customers (
	CustomerID					int,
	CustomerName				nvarchar(100),
	BillToCustomerID			int,
	CustomerCategoryID			int,
	BuyingGroupID				int,
	PrimaryContactPersonID		int,
	AlternateContactPersonID	int,
	DeliveryMethodID			int,
	DeliveryCityID				int,
	PostalCityID				int,
	CreditLimit					decimal(18,2),
	AccountOpenedDate			date,
	StandardDiscountPercentage	decimal(18,3),
	IsStatementSent				bit,
	IsOnCreditHold				bit,
	PaymentDays					int,
	PhoneNumber					nvarchar(20),
	WebsiteURL					nvarchar(256),
	DeliveryAddressLine1		nvarchar(60),
	DeliveryAddressLine2		nvarchar(60),
	DeliveryPostalCode			nvarchar(10),
	DeliveryLocation			geography,
	PostalAddressLine1			nvarchar(60),
	PostalAddressLine2			nvarchar(60),
	PostalPostalCode			nvarchar(10),
	LastEditedBy				int,
	ValidFrom					datetime2,
	ValidTo						datetime2
) AS NODE;

-- create edge table for Sales.Orders and Sales.Orderlines
-- LINK: CUSTOMERS -->> STOCKITEMS
CREATE TABLE Graph.OrderLines_CustomersToStockItems (
	
	-- from Sales.Orders
	OrderID						int,
	CustomerID					int,
	SalespersonPersonID			int,
	PickedByPersonID			int,
	ContactPersonID				int,
	BackorderOrderID			int,
	OrderDate					date,
	ExpectedDeliveryDate		date,
	CustomerPurchaseOrderNumber	nvarchar(20),
	IsUndersupplyBackordered	bit,
	Comments					nvarchar(max),
	DeliveryInstructions		nvarchar(max),
	InternalComments			nvarchar(max),

	-- from Sales.OrderLines
	StockItemID					int,
	Description					nvarchar(100),
	PackageTypeID				int,
	Quantity					int,
	UnitPrice					decimal(18,2),
	TaxRate						decimal(18,3),
	PickedQuantity				int,
	PickingCompletedWhen		datetime2,
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;

-- create edge table for Sales.Invoices and Sales.InvoiceLines
-- LINK: CUSTOMERS -->> STOCKITEMS
CREATE TABLE Graph.InvoiceLines_CustomersToStockItems (
	
	-- from Sales.Invoices
	InvoiceID					int,
	CustomerID					int,
	BillToCustomerID			int,
	OrderID						int,
	DeliveryMethodID			int,
	ContactPersonID				int,
	AccountsPersonID			int,
	SalespersonPersonID			int,
	PackedByPersonID			int,
	InvoiceDate					date,
	CustomerPurchaseOrderNumber	nvarchar(20),
	IsCreditNote				bit,
	CreditNoteReason			nvarchar(max),
	Comments					nvarchar(max),
	DeliveryInstructions		nvarchar(max),
	InternalComments			nvarchar(max),
	TotalDryItems				int,
	TotalChillerItems			int,
	DeliveryRun					nvarchar(5),
	RunPosition					nvarchar(5),
	ReturnedDeliveryData		nvarchar(max),
	ConfirmedDeliveryTime		datetime2,
	ConfirmedReceivedBy			nvarchar(4000),

	-- from Sales.InvoiceLines
	InvoiceLineID				int,
	StockItemID					int,
	Description					nvarchar(100),
	PackageTypeID				int,
	Quantity					int,
	UnitPrice					decimal(18,3),
	TaxRate						decimal(18,2),
	TaxAmount					decimal(18,2),
	LineProfit					decimal(18,2),
	ExtendedPrice				decimal(18,2),
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;


-- create edge table for Sales.Orders and Sales.Orderlines
-- LINK: STOCKITEMS -->> CUSTOMERS
CREATE TABLE Graph.OrderLines_StockItemsToCustomers (
	
	-- from Sales.Orders
	OrderID						int,
	CustomerID					int,
	SalespersonPersonID			int,
	PickedByPersonID			int,
	ContactPersonID				int,
	BackorderOrderID			int,
	OrderDate					date,
	ExpectedDeliveryDate		date,
	CustomerPurchaseOrderNumber	nvarchar(20),
	IsUndersupplyBackordered	bit,
	Comments					nvarchar(max),
	DeliveryInstructions		nvarchar(max),
	InternalComments			nvarchar(max),

	-- from Sales.OrderLines
	StockItemID					int,
	Description					nvarchar(100),
	PackageTypeID				int,
	Quantity					int,
	UnitPrice					decimal(18,2),
	TaxRate						decimal(18,3),
	PickedQuantity				int,
	PickingCompletedWhen		datetime2,
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;

-- create edge table for Sales.Invoices and Sales.InvoiceLines
-- LINK: STOCKITEMS -->> CUSTOMERS
CREATE TABLE Graph.InvoiceLines_StockItemsToCustomers (
	
	-- from Sales.Invoices
	InvoiceID					int,
	CustomerID					int,
	BillToCustomerID			int,
	OrderID						int,
	DeliveryMethodID			int,
	ContactPersonID				int,
	AccountsPersonID			int,
	SalespersonPersonID			int,
	PackedByPersonID			int,
	InvoiceDate					date,
	CustomerPurchaseOrderNumber	nvarchar(20),
	IsCreditNote				bit,
	CreditNoteReason			nvarchar(max),
	Comments					nvarchar(max),
	DeliveryInstructions		nvarchar(max),
	InternalComments			nvarchar(max),
	TotalDryItems				int,
	TotalChillerItems			int,
	DeliveryRun					nvarchar(5),
	RunPosition					nvarchar(5),
	ReturnedDeliveryData		nvarchar(max),
	ConfirmedDeliveryTime		datetime2,
	ConfirmedReceivedBy			nvarchar(4000),

	-- from Sales.InvoiceLines
	InvoiceLineID				int,
	StockItemID					int,
	Description					nvarchar(100),
	PackageTypeID				int,
	Quantity					int,
	UnitPrice					decimal(18,3),
	TaxRate						decimal(18,2),
	TaxAmount					decimal(18,2),
	LineProfit					decimal(18,2),
	ExtendedPrice				decimal(18,2),
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;


/* WAREHOUSE schema */
-- create node table for Warehouse.StockItems
CREATE TABLE Graph.StockItems (
	StockItemID					int,
	StockItemName				nvarchar(100),
	SupplierID					int,
	ColorID						int,
	UnitPackageID				int,
	OuterPackageID				int,
	Brand						nvarchar(50),
	Size						nvarchar(20),
	LeadTimeDays				int,
	QuantityPerOuter			int,
	IsChillerStock				bit,
	Barcode						nvarchar(50),
	TaxRate						decimal(18,3),
	UnitPrice					decimal(18,2),
	RecommendedRetailPrice		decimal(18,2),
	TypicalWeightPerUnit		decimal(5,2),
	MarketingComments			nvarchar(max),
	InternalComments			nvarchar(max),
	Photo						varbinary(max),
	CustomFields				nvarchar(max),
	Tags						nvarchar(max),
	SearchDetails				nvarchar(max),
	LastEditedBy				int,
	ValidFrom					datetime2,
	ValidTo						datetime2
) AS NODE;

/* PURCHASING schema */
-- create node table for Purchasing.Suppliers
CREATE TABLE Graph.Suppliers (
	SupplierID					int,
	SupplierName				nvarchar(100),
	SupplierCategoryID			int,
	PrimaryContactPersonID		int,
	AlternateContactPersonID	int,
	DeliveryMethodID			int,
	DeliveryCityID				int,
	PostalCityID				int,
	SupplierReference			nvarchar(20),
	BankAccountName				nvarchar(50),
	BankAccountBranch			nvarchar(50),
	BankAccountCode				nvarchar(20),
	BankAccountNumber			nvarchar(20),
	BankInternationalCode		nvarchar(20),
	PaymentDays					int,
	InternalComments			nvarchar(max),
	PhoneNumber					nvarchar(20),
	FaxNumber					nvarchar(20),
	WebsiteURL					nvarchar(256),
	DeliveryAddressLine1		nvarchar(60),
	DeliveryAddressLine2		nvarchar(60),
	DeliveryPostalCode			nvarchar(10),
	DeliveryLocation			geography,
	PostalAddressLine1			nvarchar(60),
	PostalAddressLine2			nvarchar(60),
	PostalPostalCode			nvarchar(10),
	LastEditedBy				int,
	ValidFrom					datetime2,
	ValidTo						datetime2
) AS NODE

-- create edge table for Purchasing.PurchaseOrders and Purchasing.PurchaseOrderLines
-- LINK: SUPPLIERS -->> STOCKITEMS
CREATE TABLE Graph.PurchaseOrderLines_SuppliersToStockItems (

	-- from Purchasing.PurchaseOrders
	PurchaseOrderID				int,
	SupplierID					int,
	OrderDate					date,
	DeliveryMethodID			int,
	ContactPersonID				int,
	ExpectedDeliveryDate		date,
	SupplierReference			nvarchar(20),
	IsOrderFinalized			bit,
	Comments					nvarchar(max),
	InternalComments			nvarchar(max),

	-- from Purchasing.PurchaseOrderLines
	PurchaseOrderLineID			int,
	StockItemID					int,
	OrderedOuters				int,
	Description					nvarchar(100),
	ReceivedOuters				int,
	PackageTypeID				int,
	ExpectedUnitPricePerOuter	decimal(18,2),
	LastReceiptDate				date,
	IsOrderLineFinalized		bit,
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;

-- create edge table for Purchasing.PurchaseOrders and Purchasing.PurchaseOrderLines
-- LINK: STOCKITEMS -->> SUPPLIERS
CREATE TABLE Graph.PurchaseOrderLines_StockItemsToSuppliers (

	-- from Purchasing.PurchaseOrders
	PurchaseOrderID				int,
	SupplierID					int,
	OrderDate					date,
	DeliveryMethodID			int,
	ContactPersonID				int,
	ExpectedDeliveryDate		date,
	SupplierReference			nvarchar(20),
	IsOrderFinalized			bit,
	Comments					nvarchar(max),
	InternalComments			nvarchar(max),

	-- from Purchasing.PurchaseOrderLines
	PurchaseOrderLineID			int,
	StockItemID					int,
	OrderedOuters				int,
	Description					nvarchar(100),
	ReceivedOuters				int,
	PackageTypeID				int,
	ExpectedUnitPricePerOuter	decimal(18,2),
	LastReceiptDate				date,
	IsOrderLineFinalized		bit,
	LastEditedBy				int,
	LastEditedWhen				datetime2
) AS EDGE;

go
