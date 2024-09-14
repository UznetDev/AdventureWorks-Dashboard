SELECT DAY(OrderDate) AS day, 
    SUM(OrderQty) AS count 
FROM `Sales_SalesOrderHeader` ssoh 
JOIN `Sales_SalesOrderDetail` ssod 
USING(SalesOrderID) 
GROUP BY day 
ORDER BY day;