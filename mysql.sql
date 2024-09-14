SELECT DAY(OrderDate) AS day, 
    SUM(OrderQty) AS count 
FROM `Sales_SalesOrderHeader` ssoh 
JOIN `Sales_SalesOrderDetail` ssod 
USING(SalesOrderID) 
GROUP BY day 
ORDER BY day;


CREATE TABLE month (
    number INT PRIMARY KEY,
    name VARCHAR(20)
);


INSERT INTO month (number, name) VALUES
(1, 'Yanvar'),
(2, 'Fevral'),
(3, 'Mart'),
(4, 'Aprel'),
(5, 'May'),
(6, 'Iyun'),
(7, 'Iyul'),
(8, 'Avgust'),
(9, 'Sentyabr'),
(10, 'Oktyabr'),
(11, 'Noyabr'),
(12, 'Dekabr');


SELECT name AS month, SUM(TotalDue) AS v
FROM `Sales_SalesOrderHeader` s
JOIN month m
ON MONTH(s.DueDate)=m.number
GROUP BY month
ORDER BY v;


ALTER TABLE Sales_SalesOrderDetail
ADD NetProfit FLOAT;

UPDATE Sales_SalesOrderDetail sod
JOIN Production_Product p ON sod.ProductID = p.ProductID
SET sod.NetProfit = sod.LineTotal - (sod.OrderQty * p.StandardCost);
