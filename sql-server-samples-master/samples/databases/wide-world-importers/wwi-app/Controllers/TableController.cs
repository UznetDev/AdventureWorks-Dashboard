using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Belgrade.SqlClient;
using MsSql.RestApi;

namespace wwi_app.Controllers
{
    public class TableController : Controller
    {
        IQueryPipe sqlQuery = null;

        public TableController(IQueryPipe sqlQueryService)
        {
            this.sqlQuery = sqlQueryService;
        }

		
        private static readonly TableSpec salesorders = new TableSpec("WebApi","SalesOrders", "OrderDate,CustomerPurchaseOrderNumber,CustomerName,ExpectedDeliveryDate,PhoneNumber,SalesPerson,OrderID");
        public async Task SalesOrders()
        {
            await this
				.Table(salesorders)
				.Process(this.sqlQuery);
        }
				
        private static readonly TableSpec purchaseorders = new TableSpec("WebApi","PurchaseOrders", "OrderDate,SupplierReference,ExpectedDeliveryDate,ContactName,ContactPhone,IsOrderFinalized,PurchaseOrderID");
        public async Task PurchaseOrders()
        {
            await this
				.Table(purchaseorders)
				.Process(this.sqlQuery);
        }
				
        private static readonly TableSpec invoices = new TableSpec("WebApi","Invoices", "InvoiceDate,CustomerPurchaseOrderNumber,CustomerName,SalesPersonName,ContactName,ContactPhone,SalesPersonEmail,InvoiceID");
        public async Task Invoices()
        {
            await this
				.Table(invoices)
				.Process(this.sqlQuery);
        }
				
        private static readonly TableSpec customertransactions = new TableSpec("WebApi","CustomerTransactions", "TransactionDate,TransactionAmount,IsFinalized,CustomerName,TransactionTypeName,PaymentMethodName,InvoiceDate,CustomerTransactionID");
        public async Task CustomerTransactions()
        {
            await this
				.Table(customertransactions)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec suppliertransactions = new TableSpec("WebApi","SupplierTransactions", "TransactionDate,TransactionAmount,IsFinalized,SupplierName,TransactionTypeName,PaymentMethodName,SupplierTransactionID");
        public async Task SupplierTransactions()
        {
            await this
				.Table(suppliertransactions)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec customers = new TableSpec("WebApi","Customers", "CustomerName,CustomerCategoryName,PhoneNumber,FaxNumber,BuyingGroupName,CustomerID");
        public async Task Customers()
        {
            await this
				.Table(customers)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec suppliers = new TableSpec("WebApi","Suppliers", "SupplierName,SupplierCategoryName,PhoneNumber,FaxNumber,PrimaryContact,SupplierID");
        public async Task Suppliers()
        {
            await this
				.Table(suppliers)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec countries = new TableSpec("WebApi","Countries", "FormalName,Subregion,Region,Continent,LatestRecordedPopulation,CountryID");
        public async Task Countries()
        {
            await this
				.Table(countries)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec cities = new TableSpec("WebApi","Cities", "CityName,LatestRecordedPopulation,StateProvinceName,CityID");
        public async Task Cities()
        {
            await this
				.Table(cities)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec stateprovinces = new TableSpec("WebApi","StateProvinces", "StateProvinceName,StateProvinceCode,SalesTerritory,LatestRecordedPopulation,CountryName,StateProvinceID");
        public async Task StateProvinces()
        {
            await this
				.Table(stateprovinces)
				.Process(this.sqlQuery);
        }
		
        private static readonly TableSpec stockitems = new TableSpec("WebApi","StockItems", "StockItemName,SupplierName,UnitPrice,TaxRate,RecommendedRetailPrice,StockItemID");
        public async Task StockItems()
        {
            await this
				.Table(stockitems)
				.Process(this.sqlQuery);
        }
																		    }
}

