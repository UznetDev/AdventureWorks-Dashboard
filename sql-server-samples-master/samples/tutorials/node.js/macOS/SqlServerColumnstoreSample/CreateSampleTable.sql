WITH a AS (SELECT * FROM (VALUES(1),(2),(3),(4),(5),(6),(7),(8),(9),(10)) AS a(a))
SELECT TOP(5000000)
ROW_NUMBER() OVER (ORDER BY a.a) AS OrderItemId
,a.a + b.a + c.a + d.a + e.a + f.a + g.a + h.a AS OrderId
,a.a * 10 AS Price
,CONCAT(a.a, N' ', b.a, N' ', c.a, N' ', d.a, N' ', e.a, N' ', f.a, N' ', g.a, N' ', h.a) AS ProductName
INTO Table_with_5M_rows
FROM a, a AS b, a AS c, a AS d, a AS e, a AS f, a AS g, a AS h;