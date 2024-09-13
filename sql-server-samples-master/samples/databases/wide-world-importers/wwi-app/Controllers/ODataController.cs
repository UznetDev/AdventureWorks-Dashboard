using Belgrade.SqlClient;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MsSql.RestApi;
using System;
using System.IO;
using System.Security.Claims;
using System.Threading.Tasks;

namespace wwi_app.Controllers
{
    public partial class ODataController : Controller
    {
		ICommand sqlCmd = null;

        public ODataController(ICommand sqlCommandService)
        {
			this.sqlCmd = sqlCommandService;
        }


		TableSpec salesorders = new TableSpec("WebApi","SalesOrders", "OrderID,OrderDate,CustomerPurchaseOrderNumber,ExpectedDeliveryDate,PickingCompletedWhen,CustomerID,CustomerName,PhoneNumber,FaxNumber,WebsiteURL,DeliveryLocation,SalesPerson,SalesPersonPhone,SalesPersonEmail");

		[HttpGet]
        public async Task SalesOrders(int? id)
        {
			await this.OData(salesorders, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task SalesOrders(int id, string body)
        {
            var SalesOrder = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSalesOrderFromJson @SalesOrder, @SalesOrderID = {id}, @UserID = @UserID")
				.Param("SalesOrder", SalesOrder)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task SalesOrders()
        {
            var SalesOrders = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSalesOrdersFromJson @SalesOrders, @UserID = @UserID")
				.Param("SalesOrders", SalesOrders)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task SalesOrders(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSalesOrder @SalesOrderID = {id}").Exec();
        }


		TableSpec salesorderlines = new TableSpec("WebApi","SalesOrderLines", "OrderLineID,OrderID,Description,Quantity,UnitPrice,TaxRate,ProductName,Brand,Size,ColorName,PackageTypeName,PickingCompletedWhen");

		[HttpGet]
        public async Task SalesOrderLines(int? id)
        {
			await this.OData(salesorderlines, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task SalesOrderLines(int id, string body)
        {
            var SalesOrderLine = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSalesOrderLineFromJson @SalesOrderLine, @SalesOrderLineID = {id}, @UserID = @UserID")
				.Param("SalesOrderLine", SalesOrderLine)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task SalesOrderLines()
        {
            var SalesOrderLines = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSalesOrderLinesFromJson @SalesOrderLines, @UserID = @UserID")
				.Param("SalesOrderLines", SalesOrderLines)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task SalesOrderLines(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSalesOrderLine @SalesOrderLineID = {id}").Exec();
        }


		TableSpec purchaseorders = new TableSpec("WebApi","PurchaseOrders", "PurchaseOrderID,OrderDate,ExpectedDeliveryDate,SupplierReference,IsOrderFinalized,DeliveryMethodName,ContactName,ContactPhone,ContactFax,ContactEmail,SupplierID");

		[HttpGet]
        public async Task PurchaseOrders(int? id)
        {
			await this.OData(purchaseorders, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task PurchaseOrders(int id, string body)
        {
            var PurchaseOrder = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdatePurchaseOrderFromJson @PurchaseOrder, @PurchaseOrderID = {id}, @UserID = @UserID")
				.Param("PurchaseOrder", PurchaseOrder)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task PurchaseOrders()
        {
            var PurchaseOrders = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertPurchaseOrdersFromJson @PurchaseOrders, @UserID = @UserID")
				.Param("PurchaseOrders", PurchaseOrders)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task PurchaseOrders(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeletePurchaseOrder @PurchaseOrderID = {id}").Exec();
        }


		TableSpec purchaseorderlines = new TableSpec("WebApi","PurchaseOrderLines", "PurchaseOrderLineID,PurchaseOrderID,Description,IsOrderLineFinalized,ProductName,Brand,Size,ColorName,PackageTypeName,OrderedOuters,ReceivedOuters,ExpectedUnitPricePerOuter");

		[HttpGet]
        public async Task PurchaseOrderLines(int? id)
        {
			await this.OData(purchaseorderlines, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task PurchaseOrderLines(int id, string body)
        {
            var PurchaseOrderLine = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdatePurchaseOrderLineFromJson @PurchaseOrderLine, @PurchaseOrderLineID = {id}, @UserID = @UserID")
				.Param("PurchaseOrderLine", PurchaseOrderLine)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task PurchaseOrderLines()
        {
            var PurchaseOrderLines = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertPurchaseOrderLinesFromJson @PurchaseOrderLines, @UserID = @UserID")
				.Param("PurchaseOrderLines", PurchaseOrderLines)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task PurchaseOrderLines(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeletePurchaseOrderLine @PurchaseOrderLineID = {id}").Exec();
        }


		TableSpec invoices = new TableSpec("WebApi","Invoices", "InvoiceID,InvoiceDate,CustomerPurchaseOrderNumber,IsCreditNote,TotalDryItems,TotalChillerItems,DeliveryRun,RunPosition,ReturnedDeliveryData,ConfirmedDeliveryTime,ConfirmedReceivedBy,CustomerName,SalesPersonName,ContactName,ContactPhone,ContactEmail,SalesPersonEmail,DeliveryMethodName,CustomerID,OrderID,DeliveryMethodID,ContactPersonID,AccountsPersonID,SalespersonPersonID,PackedByPersonID");

		[HttpGet]
        public async Task Invoices(int? id)
        {
			await this.OData(invoices, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Invoices(int id, string body)
        {
            var Invoice = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateInvoiceFromJson @Invoice, @InvoiceID = {id}, @UserID = @UserID")
				.Param("Invoice", Invoice)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Invoices()
        {
            var Invoices = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertInvoicesFromJson @Invoices, @UserID = @UserID")
				.Param("Invoices", Invoices)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Invoices(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteInvoice @InvoiceID = {id}").Exec();
        }


		TableSpec specialdeals = new TableSpec("WebApi","SpecialDeals", "SpecialDealID,DealDescription,StartDate,EndDate,DiscountAmount,DiscountPercentage,UnitPrice,StockItemName,Brand,Size,CustomerName,BuyingGroupName,CustomerCategoryName,StockItemID,CustomerID,BuyingGroupID,CustomerCategoryID,StockGroupID");

		[HttpGet]
        public async Task SpecialDeals(int? id)
        {
			await this.OData(specialdeals, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task SpecialDeals(int id, string body)
        {
            var SpecialDeal = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSpecialDealFromJson @SpecialDeal, @SpecialDealID = {id}, @UserID = @UserID")
				.Param("SpecialDeal", SpecialDeal)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task SpecialDeals()
        {
            var SpecialDeals = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSpecialDealsFromJson @SpecialDeals, @UserID = @UserID")
				.Param("SpecialDeals", SpecialDeals)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task SpecialDeals(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSpecialDeal @SpecialDealID = {id}").Exec();
        }


		TableSpec customertransactions = new TableSpec("WebApi","CustomerTransactions", "CustomerTransactionID,TransactionDate,AmountExcludingTax,TaxAmount,TransactionAmount,OutstandingBalance,FinalizationDate,IsFinalized,CustomerName,TransactionTypeName,InvoiceDate,CustomerPurchaseOrderNumber,PaymentMethodName,CustomerID,TransactionTypeID,InvoiceID,PaymentMethodID");

		[HttpGet]
        public async Task CustomerTransactions(int? id)
        {
			await this.OData(customertransactions, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task CustomerTransactions(int id, string body)
        {
            var CustomerTransaction = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateCustomerTransactionFromJson @CustomerTransaction, @CustomerTransactionID = {id}, @UserID = @UserID")
				.Param("CustomerTransaction", CustomerTransaction)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task CustomerTransactions()
        {
            var CustomerTransactions = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertCustomerTransactionsFromJson @CustomerTransactions, @UserID = @UserID")
				.Param("CustomerTransactions", CustomerTransactions)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task CustomerTransactions(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteCustomerTransaction @CustomerTransactionID = {id}").Exec();
        }


		TableSpec suppliertransactions = new TableSpec("WebApi","SupplierTransactions", "SupplierTransactionID,TransactionDate,AmountExcludingTax,TaxAmount,TransactionAmount,OutstandingBalance,FinalizationDate,IsFinalized,SupplierName,TransactionTypeName,PaymentMethodName,SupplierID,TransactionTypeID,PurchaseOrderID,PaymentMethodID,OrderDate,IsOrderFinalized,ExpectedDeliveryDate,SupplierReference");

		[HttpGet]
        public async Task SupplierTransactions(int? id)
        {
			await this.OData(suppliertransactions, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task SupplierTransactions(int id, string body)
        {
            var SupplierTransaction = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSupplierTransactionFromJson @SupplierTransaction, @SupplierTransactionID = {id}, @UserID = @UserID")
				.Param("SupplierTransaction", SupplierTransaction)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task SupplierTransactions()
        {
            var SupplierTransactions = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSupplierTransactionsFromJson @SupplierTransactions, @UserID = @UserID")
				.Param("SupplierTransactions", SupplierTransactions)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task SupplierTransactions(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSupplierTransaction @SupplierTransactionID = {id}").Exec();
        }


		TableSpec customers = new TableSpec("WebApi","Customers", "CustomerID,CustomerName,AccountOpenedDate,CustomerCategoryName,PrimaryContact,AlternateContact,PhoneNumber,FaxNumber,WebsiteURL,PostalAddressLine1,PostalAddressLine2,PostalCity,PostalCityID,PostalPostalCode,CreditLimit,IsOnCreditHold,IsStatementSent,PaymentDays,RunPosition,StandardDiscountPercentage,BuyingGroupName,DeliveryLocation,BuyingGroupID,BillToCustomerID,CustomerCategoryID,PrimaryContactPersonID,AlternateContactPersonID");

		[HttpGet]
        public async Task Customers(int? id)
        {
			await this.OData(customers, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Customers(int id, string body)
        {
            var Customer = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateCustomerFromJson @Customer, @CustomerID = {id}, @UserID = @UserID")
				.Param("Customer", Customer)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Customers()
        {
            var Customers = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertCustomersFromJson @Customers, @UserID = @UserID")
				.Param("Customers", Customers)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Customers(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteCustomer @CustomerID = {id}").Exec();
        }


		TableSpec suppliers = new TableSpec("WebApi","Suppliers", "SupplierID,SupplierName,SupplierCategoryName,PrimaryContact,AlternateContact,PhoneNumber,FaxNumber,WebsiteURL,SupplierReference,DeliveryLocation,BankAccountName,BankAccountBranch,BankAccountCode,BankAccountNumber,BankInternationalCode,PostalAddressLine1,PostalAddressLine2,PostalPostalCode,PaymentDays,SupplierCategoryID");

		[HttpGet]
        public async Task Suppliers(int? id)
        {
			await this.OData(suppliers, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Suppliers(int id, string body)
        {
            var Supplier = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSupplierFromJson @Supplier, @SupplierID = {id}, @UserID = @UserID")
				.Param("Supplier", Supplier)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Suppliers()
        {
            var Suppliers = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSuppliersFromJson @Suppliers, @UserID = @UserID")
				.Param("Suppliers", Suppliers)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Suppliers(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSupplier @SupplierID = {id}").Exec();
        }


		TableSpec countries = new TableSpec("WebApi","Countries", "CountryID,CountryName,FormalName,IsoAlpha3Code,IsoNumericCode,CountryType,LatestRecordedPopulation,Continent,Region,Subregion");

		[HttpGet]
        public async Task Countries(int? id)
        {
			await this.OData(countries, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Countries(int id, string body)
        {
            var Country = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateCountryFromJson @Country, @CountryID = {id}, @UserID = @UserID")
				.Param("Country", Country)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Countries()
        {
            var Countries = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertCountriesFromJson @Countries, @UserID = @UserID")
				.Param("Countries", Countries)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Countries(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteCountry @CountryID = {id}").Exec();
        }


		TableSpec cities = new TableSpec("WebApi","Cities", "CityID,CityName,StateProvinceID,LatestRecordedPopulation");

		[HttpGet]
        public async Task Cities(int? id)
        {
			await this.OData(cities, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Cities(int id, string body)
        {
            var City = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateCityFromJson @City, @CityID = {id}, @UserID = @UserID")
				.Param("City", City)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Cities()
        {
            var Cities = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertCitiesFromJson @Cities, @UserID = @UserID")
				.Param("Cities", Cities)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Cities(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteCity @CityID = {id}").Exec();
        }


		TableSpec stateprovinces = new TableSpec("WebApi","StateProvinces", "StateProvinceID,StateProvinceCode,StateProvinceName,CountryID,SalesTerritory,LatestRecordedPopulation");

		[HttpGet]
        public async Task StateProvinces(int? id)
        {
			await this.OData(stateprovinces, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task StateProvinces(int id, string body)
        {
            var StateProvince = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateStateProvinceFromJson @StateProvince, @StateProvinceID = {id}, @UserID = @UserID")
				.Param("StateProvince", StateProvince)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task StateProvinces()
        {
            var StateProvinces = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertStateProvincesFromJson @StateProvinces, @UserID = @UserID")
				.Param("StateProvinces", StateProvinces)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task StateProvinces(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteStateProvince @StateProvinceID = {id}").Exec();
        }


		TableSpec stockitems = new TableSpec("WebApi","StockItems", "StockItemID,StockItemName,SupplierName,SupplierReference,ColorName,OuterPackage,UnitPackage,Brand,Size,LeadTimeDays,QuantityPerOuter,IsChillerStock,Barcode,TaxRate,UnitPrice,RecommendedRetailPrice,TypicalWeightPerUnit,MarketingComments,InternalComments,CustomFields,QuantityOnHand,BinLocation,LastStocktakeQuantity,LastCostPrice,ReorderLevel,TargetStockLevel,SupplierID,ColorID,UnitPackageID,OuterPackageID");

		[HttpGet]
        public async Task StockItems(int? id)
        {
			await this.OData(stockitems, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task StockItems(int id, string body)
        {
            var StockItem = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateStockItemFromJson @StockItem, @StockItemID = {id}, @UserID = @UserID")
				.Param("StockItem", StockItem)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task StockItems()
        {
            var StockItems = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertStockItemsFromJson @StockItems, @UserID = @UserID")
				.Param("StockItems", StockItems)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task StockItems(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteStockItem @StockItemID = {id}").Exec();
        }


		TableSpec packagetypes = new TableSpec("WebApi","PackageTypes", "PackageTypeID,PackageTypeName");

		[HttpGet]
        public async Task PackageTypes(int? id)
        {
			await this.OData(packagetypes, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task PackageTypes(int id, string body)
        {
            var PackageType = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdatePackageTypeFromJson @PackageType, @PackageTypeID = {id}, @UserID = @UserID")
				.Param("PackageType", PackageType)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task PackageTypes()
        {
            var PackageTypes = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertPackageTypesFromJson @PackageTypes, @UserID = @UserID")
				.Param("PackageTypes", PackageTypes)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task PackageTypes(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeletePackageType @PackageTypeID = {id}").Exec();
        }


		TableSpec colors = new TableSpec("WebApi","Colors", "ColorID,ColorName");

		[HttpGet]
        public async Task Colors(int? id)
        {
			await this.OData(colors, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task Colors(int id, string body)
        {
            var Color = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateColorFromJson @Color, @ColorID = {id}, @UserID = @UserID")
				.Param("Color", Color)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task Colors()
        {
            var Colors = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertColorsFromJson @Colors, @UserID = @UserID")
				.Param("Colors", Colors)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task Colors(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteColor @ColorID = {id}").Exec();
        }


		TableSpec stockgroups = new TableSpec("WebApi","StockGroups", "StockGroupID,StockGroupName");

		[HttpGet]
        public async Task StockGroups(int? id)
        {
			await this.OData(stockgroups, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task StockGroups(int id, string body)
        {
            var StockGroup = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateStockGroupFromJson @StockGroup, @StockGroupID = {id}, @UserID = @UserID")
				.Param("StockGroup", StockGroup)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task StockGroups()
        {
            var StockGroups = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertStockGroupsFromJson @StockGroups, @UserID = @UserID")
				.Param("StockGroups", StockGroups)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task StockGroups(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteStockGroup @StockGroupID = {id}").Exec();
        }


		TableSpec buyinggroups = new TableSpec("WebApi","BuyingGroups", "BuyingGroupID,BuyingGroupName");

		[HttpGet]
        public async Task BuyingGroups(int? id)
        {
			await this.OData(buyinggroups, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task BuyingGroups(int id, string body)
        {
            var BuyingGroup = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateBuyingGroupFromJson @BuyingGroup, @BuyingGroupID = {id}, @UserID = @UserID")
				.Param("BuyingGroup", BuyingGroup)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task BuyingGroups()
        {
            var BuyingGroups = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertBuyingGroupsFromJson @BuyingGroups, @UserID = @UserID")
				.Param("BuyingGroups", BuyingGroups)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task BuyingGroups(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteBuyingGroup @BuyingGroupID = {id}").Exec();
        }


		TableSpec customercategories = new TableSpec("WebApi","CustomerCategories", "CustomerCategoryID,CustomerCategoryName");

		[HttpGet]
        public async Task CustomerCategories(int? id)
        {
			await this.OData(customercategories, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task CustomerCategories(int id, string body)
        {
            var CustomerCategory = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateCustomerCategoryFromJson @CustomerCategory, @CustomerCategoryID = {id}, @UserID = @UserID")
				.Param("CustomerCategory", CustomerCategory)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task CustomerCategories()
        {
            var CustomerCategories = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertCustomerCategoriesFromJson @CustomerCategories, @UserID = @UserID")
				.Param("CustomerCategories", CustomerCategories)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task CustomerCategories(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteCustomerCategory @CustomerCategoryID = {id}").Exec();
        }


		TableSpec suppliercategories = new TableSpec("WebApi","SupplierCategories", "SupplierCategoryID,SupplierCategoryName");

		[HttpGet]
        public async Task SupplierCategories(int? id)
        {
			await this.OData(suppliercategories, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task SupplierCategories(int id, string body)
        {
            var SupplierCategory = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateSupplierCategoryFromJson @SupplierCategory, @SupplierCategoryID = {id}, @UserID = @UserID")
				.Param("SupplierCategory", SupplierCategory)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task SupplierCategories()
        {
            var SupplierCategories = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertSupplierCategoriesFromJson @SupplierCategories, @UserID = @UserID")
				.Param("SupplierCategories", SupplierCategories)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task SupplierCategories(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteSupplierCategory @SupplierCategoryID = {id}").Exec();
        }


		TableSpec transactiontypes = new TableSpec("WebApi","TransactionTypes", "TransactionTypeID,TransactionTypeName");

		[HttpGet]
        public async Task TransactionTypes(int? id)
        {
			await this.OData(transactiontypes, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task TransactionTypes(int id, string body)
        {
            var TransactionType = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateTransactionTypeFromJson @TransactionType, @TransactionTypeID = {id}, @UserID = @UserID")
				.Param("TransactionType", TransactionType)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task TransactionTypes()
        {
            var TransactionTypes = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertTransactionTypesFromJson @TransactionTypes, @UserID = @UserID")
				.Param("TransactionTypes", TransactionTypes)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task TransactionTypes(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteTransactionType @TransactionTypeID = {id}").Exec();
        }


		TableSpec paymentmethods = new TableSpec("WebApi","PaymentMethods", "PaymentMethodID,PaymentMethodName");

		[HttpGet]
        public async Task PaymentMethods(int? id)
        {
			await this.OData(paymentmethods, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task PaymentMethods(int id, string body)
        {
            var PaymentMethod = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdatePaymentMethodFromJson @PaymentMethod, @PaymentMethodID = {id}, @UserID = @UserID")
				.Param("PaymentMethod", PaymentMethod)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task PaymentMethods()
        {
            var PaymentMethods = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertPaymentMethodsFromJson @PaymentMethods, @UserID = @UserID")
				.Param("PaymentMethods", PaymentMethods)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task PaymentMethods(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeletePaymentMethod @PaymentMethodID = {id}").Exec();
        }


		TableSpec deliverymethods = new TableSpec("WebApi","DeliveryMethods", "DeliveryMethodID,DeliveryMethodName");

		[HttpGet]
        public async Task DeliveryMethods(int? id)
        {
			await this.OData(deliverymethods, id: id).Process(this.sqlCmd);
        }
		
        [Authorize]
		[HttpPut]
        public async Task DeliveryMethods(int id, string body)
        {
            var DeliveryMethod = new StreamReader(Request.Body).ReadToEnd();

			await sqlCmd
				.Sql($"EXEC WebApi.UpdateDeliveryMethodFromJson @DeliveryMethod, @DeliveryMethodID = {id}, @UserID = @UserID")
				.Param("DeliveryMethod", DeliveryMethod)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

        [Authorize]
        [HttpPost]
        public async Task DeliveryMethods()
        {
            var DeliveryMethods = new StreamReader(Request.Body).ReadToEnd();
			await sqlCmd
				.Sql($"EXEC WebApi.InsertDeliveryMethodsFromJson @DeliveryMethods, @UserID = @UserID")
				.Param("DeliveryMethods", DeliveryMethods)
				.Param("UserID", Convert.ToInt32(this.User.FindFirst(ClaimTypes.Sid).Value))
				.Exec();
        }

		[Authorize]
        [HttpDelete]
        public async Task DeliveryMethods(int id)
        {
            await this.sqlCmd.Sql($"EXEC WebApi.DeleteDeliveryMethod @DeliveryMethodID = {id}").Exec();
        }



    }
}

