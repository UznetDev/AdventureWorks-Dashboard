using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using MsSql.RestApi;
using System;
using System.Threading.Tasks;

namespace WideWorldImportersFunctions
{
    public static class OData
    {
        [FunctionName("SalesOrders")]
        public static async Task<IActionResult> SalesOrders(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec salesorders = new TableSpec(schema: "WebApi", table: "SalesOrders", columns: "OrderID,OrderDate,CustomerPurchaseOrderNumber,ExpectedDeliveryDate,PickingCompletedWhen,CustomerID,CustomerName,PhoneNumber,FaxNumber,WebsiteURL,DeliveryLocation,SalesPerson,SalesPersonPhone,SalesPersonEmail");
                return await req.OData(salesorders).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("SalesOrderLines")]
        public static async Task<IActionResult> SalesOrderLines(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec salesorderlines = new TableSpec(schema: "WebApi", table: "SalesOrderLines", columns: "OrderLineID,OrderID,Description,Quantity,UnitPrice,TaxRate,ProductName,Brand,Size,ColorName,PackageTypeName,PickingCompletedWhen");
                return await req.OData(salesorderlines).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("PurchaseOrders")]
        public static async Task<IActionResult> PurchaseOrders(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec purchaseorders = new TableSpec(schema: "WebApi", table: "PurchaseOrders", columns: "PurchaseOrderID,OrderDate,ExpectedDeliveryDate,SupplierReference,IsOrderFinalized,DeliveryMethodName,ContactName,ContactPhone,ContactFax,ContactEmail,SupplierID");
                return await req.OData(purchaseorders).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("PurchaseOrderLines")]
        public static async Task<IActionResult> PurchaseOrderLines(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec purchaseorderlines = new TableSpec(schema: "WebApi", table: "PurchaseOrderLines", columns: "PurchaseOrderLineID,PurchaseOrderID,Description,IsOrderLineFinalized,ProductName,Brand,Size,ColorName,PackageTypeName,OrderedOuters,ReceivedOuters,ExpectedUnitPricePerOuter");
                return await req.OData(purchaseorderlines).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Invoices")]
        public static async Task<IActionResult> Invoices(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec invoices = new TableSpec(schema: "WebApi", table: "Invoices", columns: "InvoiceID,InvoiceDate,CustomerPurchaseOrderNumber,IsCreditNote,TotalDryItems,TotalChillerItems,DeliveryRun,RunPosition,ReturnedDeliveryData,ConfirmedDeliveryTime,ConfirmedReceivedBy,CustomerName,SalesPersonName,ContactName,ContactPhone,ContactEmail,SalesPersonEmail,DeliveryMethodName,CustomerID,OrderID,DeliveryMethodID,ContactPersonID,AccountsPersonID,SalespersonPersonID,PackedByPersonID");
                return await req.OData(invoices).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("SpecialDeals")]
        public static async Task<IActionResult> SpecialDeals(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec specialdeals = new TableSpec(schema: "WebApi", table: "SpecialDeals", columns: "SpecialDealID,DealDescription,StartDate,EndDate,DiscountAmount,DiscountPercentage,UnitPrice,StockItemName,Brand,Size,CustomerName,BuyingGroupName,CustomerCategoryName,StockItemID,CustomerID,BuyingGroupID,CustomerCategoryID,StockGroupID");
                return await req.OData(specialdeals).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("CustomerTransactions")]
        public static async Task<IActionResult> CustomerTransactions(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec customertransactions = new TableSpec(schema: "WebApi", table: "CustomerTransactions", columns: "CustomerTransactionID,TransactionDate,AmountExcludingTax,TaxAmount,TransactionAmount,OutstandingBalance,FinalizationDate,IsFinalized,CustomerName,TransactionTypeName,InvoiceDate,CustomerPurchaseOrderNumber,PaymentMethodName,CustomerID,TransactionTypeID,InvoiceID,PaymentMethodID");
                return await req.OData(customertransactions).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("SupplierTransactions")]
        public static async Task<IActionResult> SupplierTransactions(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec suppliertransactions = new TableSpec(schema: "WebApi", table: "SupplierTransactions", columns: "SupplierTransactionID,TransactionDate,AmountExcludingTax,TaxAmount,TransactionAmount,OutstandingBalance,FinalizationDate,IsFinalized,SupplierName,TransactionTypeName,PaymentMethodName,SupplierID,TransactionTypeID,PurchaseOrderID,PaymentMethodID,OrderDate,IsOrderFinalized,ExpectedDeliveryDate,SupplierReference");
                return await req.OData(suppliertransactions).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Customers")]
        public static async Task<IActionResult> Customers(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec customers = new TableSpec(schema: "WebApi", table: "Customers", columns: "CustomerID,CustomerName,AccountOpenedDate,CustomerCategoryName,PrimaryContact,AlternateContact,PhoneNumber,FaxNumber,WebsiteURL,PostalAddressLine1,PostalAddressLine2,PostalCity,PostalCityID,PostalPostalCode,CreditLimit,IsOnCreditHold,IsStatementSent,PaymentDays,RunPosition,StandardDiscountPercentage,BuyingGroupName,DeliveryLocation,BuyingGroupID,BillToCustomerID,CustomerCategoryID,PrimaryContactPersonID,AlternateContactPersonID");
                return await req.OData(customers).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Suppliers")]
        public static async Task<IActionResult> Suppliers(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec suppliers = new TableSpec(schema: "WebApi", table: "Suppliers", columns: "SupplierID,SupplierName,SupplierCategoryName,PrimaryContact,AlternateContact,PhoneNumber,FaxNumber,WebsiteURL,SupplierReference,DeliveryLocation,BankAccountName,BankAccountBranch,BankAccountCode,BankAccountNumber,BankInternationalCode,PostalAddressLine1,PostalAddressLine2,PostalPostalCode,PaymentDays,SupplierCategoryID");
                return await req.OData(suppliers).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Countries")]
        public static async Task<IActionResult> Countries(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec countries = new TableSpec(schema: "WebApi", table: "Countries", columns: "CountryID,CountryName,FormalName,IsoAlpha3Code,IsoNumericCode,CountryType,LatestRecordedPopulation,Continent,Region,Subregion");
                return await req.OData(countries).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Cities")]
        public static async Task<IActionResult> Cities(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec cities = new TableSpec(schema: "WebApi", table: "Cities", columns: "CityID,CityName,StateProvinceID,LatestRecordedPopulation");
                return await req.OData(cities).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("StateProvinces")]
        public static async Task<IActionResult> StateProvinces(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec stateprovinces = new TableSpec(schema: "WebApi", table: "StateProvinces", columns: "StateProvinceID,StateProvinceCode,StateProvinceName,CountryID,SalesTerritory,LatestRecordedPopulation");
                return await req.OData(stateprovinces).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("StockItems")]
        public static async Task<IActionResult> StockItems(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec stockitems = new TableSpec(schema: "WebApi", table: "StockItems", columns: "StockItemID,StockItemName,SupplierName,SupplierReference,ColorName,OuterPackage,UnitPackage,Brand,Size,LeadTimeDays,QuantityPerOuter,IsChillerStock,Barcode,TaxRate,UnitPrice,RecommendedRetailPrice,TypicalWeightPerUnit,MarketingComments,InternalComments,CustomFields,QuantityOnHand,BinLocation,LastStocktakeQuantity,LastCostPrice,ReorderLevel,TargetStockLevel,SupplierID,ColorID,UnitPackageID,OuterPackageID");
                return await req.OData(stockitems).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("PackageTypes")]
        public static async Task<IActionResult> PackageTypes(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec packagetypes = new TableSpec(schema: "WebApi", table: "PackageTypes", columns: "PackageTypeID,PackageTypeName");
                return await req.OData(packagetypes).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("Colors")]
        public static async Task<IActionResult> Colors(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec colors = new TableSpec(schema: "WebApi", table: "Colors", columns: "ColorID,ColorName");
                return await req.OData(colors).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("StockGroups")]
        public static async Task<IActionResult> StockGroups(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec stockgroups = new TableSpec(schema: "WebApi", table: "StockGroups", columns: "StockGroupID,StockGroupName");
                return await req.OData(stockgroups).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("BuyingGroups")]
        public static async Task<IActionResult> BuyingGroups(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec buyinggroups = new TableSpec(schema: "WebApi", table: "BuyingGroups", columns: "BuyingGroupID,BuyingGroupName");
                return await req.OData(buyinggroups).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("CustomerCategories")]
        public static async Task<IActionResult> CustomerCategories(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec customercategories = new TableSpec(schema: "WebApi", table: "CustomerCategories", columns: "CustomerCategoryID,CustomerCategoryName");
                return await req.OData(customercategories).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("SupplierCategories")]
        public static async Task<IActionResult> SupplierCategories(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec suppliercategories = new TableSpec(schema: "WebApi", table: "SupplierCategories", columns: "SupplierCategoryID,SupplierCategoryName");
                return await req.OData(suppliercategories).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("TransactionTypes")]
        public static async Task<IActionResult> TransactionTypes(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec transactiontypes = new TableSpec(schema: "WebApi", table: "TransactionTypes", columns: "TransactionTypeID,TransactionTypeName");
                return await req.OData(transactiontypes).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("PaymentMethods")]
        public static async Task<IActionResult> PaymentMethods(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec paymentmethods = new TableSpec(schema: "WebApi", table: "PaymentMethods", columns: "PaymentMethodID,PaymentMethodName");
                return await req.OData(paymentmethods).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

        [FunctionName("DeliveryMethods")]
        public static async Task<IActionResult> DeliveryMethods(
            [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = null)] HttpRequest req, ILogger log)
        {
            log.LogInformation("C# HTTP trigger function processed a request.");
            try
            {
                TableSpec deliverymethods = new TableSpec(schema: "WebApi", table: "DeliveryMethods", columns: "DeliveryMethodID,DeliveryMethodName");
                return await req.OData(deliverymethods).GetResult(Environment.GetEnvironmentVariable("SqlDb"));
            }
            catch (Exception ex)
            {
                log.LogError($"C# Http trigger function exception: {ex.Message}");
                return new StatusCodeResult(500);
            }
        }

    }
}
