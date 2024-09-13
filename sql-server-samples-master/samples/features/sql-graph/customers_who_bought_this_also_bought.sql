/*
Customer who bought this also bought this
Using graph tables
Using regular tables
*/

-- using graph tables
SELECT DISTINCT s2.StockItemName
FROM Graph.StockItems AS s1, Graph.OrderLines_CustomersToStockItems, Graph.Customers, Graph.OrderLines_StockItemsToCustomers, Graph.StockItems AS s2
WHERE MATCH (s1 - (OrderLines_StockItemsToCustomers) -> Customers and Customers - (OrderLines_CustomersToStockItems) -> s2)
	and s1.StockItemName = 'Chocolate frogs 250g'
ORDER BY s2.StockItemName
go

-- using regular tables
SELECT DISTINCT s2.StockItemName
FROM (select StockItemID, StockItemName FROM Warehouse.StockItems ) AS s1
	join (select StockItemID, OrderID FROM Sales.OrderLines) AS q1 ON q1.StockItemID = s1.StockItemID
	join (select OrderID, CustomerID FROM Sales.Orders) AS q2 ON q1.OrderID = q2.OrderID
	join (select CustomerID, OrderID FROM Sales.Orders) AS q3 ON q2.CustomerID = q3.CustomerID
	join (select OrderID, StockItemID FROM Sales.Orderlines) AS q4 ON q3.OrderID = q4.OrderID
	join (select StockItemID, StockItemName FROM Warehouse.StockItems ) AS s2 ON q4.StockItemID = s2.StockItemID
WHERE s1.StockItemName = 'Chocolate frogs 250g'
ORDER BY s2.StockItemName
go


