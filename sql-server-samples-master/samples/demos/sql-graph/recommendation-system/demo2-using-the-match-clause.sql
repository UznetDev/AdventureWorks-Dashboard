------------------------------------------------------------------------
-- Event:        SQL Saturday #675 Parma, November 18 2017             -
--               http://www.sqlsaturday.com/675/EventHome.aspx         -
-- Session:      SQL Server 2017 Graph Database                        -
-- Demo:         Demo1: Using the MATCH clause                         -
-- Author:       Sergio Govoni                                         -
-- Notes:        --                                                    -
------------------------------------------------------------------------

USE [WideWorldImporters];
GO


SELECT * FROM Edges.Friends;

-- List of all guys that speak finnish with friends
-- Pattern: Node > Relationship > Node
SELECT
  P1.FullName
  ,P1.[Language]
  ,Friends_Number = COUNT(*)
FROM
  Nodes.Person AS P1
  ,Edges.Friends AS Friends
  ,Nodes.Person AS P2
WHERE
  MATCH(P1-(Friends)->P2)
  AND (P1.[Language] = 'Finnish')
GROUP BY
  P1.FullName, P1.[Language]
ORDER BY
  Friends_Number DESC, P1.[Language];
GO




-- List of the top 5 people who have friends that speak Greek
-- in the first and second connections
SELECT
  TOP 5
  P1.FullName
  ,P1.[Language]
  ,GreekFriends = COUNT(*)
FROM
  Nodes.Person AS P1
  ,Edges.Friends AS F1
  ,Nodes.Person AS P2
  ,Edges.Friends AS F2
  ,Nodes.Person AS P3
WHERE
  MATCH(P1-(F1)-> P2-(F2)-> P3)
  AND ((P2.[Language] = 'Greek') OR (P3.[Language] = 'Greek'))
GROUP BY
  P1.FullName, P1.[Language]
ORDER BY
  GreekFriends DESC, P1.[Language];
GO


-- People who have common friends that speak Croatian
SELECT
  P1.FullName
  ,P2.FullName
  ,P2.[Language]
  --,P3.FullName
FROM
  Nodes.Person AS P1
  ,Edges.Friends AS F1
  ,Nodes.Person AS P2
  ,Edges.Friends AS F2
  ,Nodes.Person AS P3
WHERE
  MATCH(P1-(F1)-> P2 <-(F2)-P3)
  AND (P2.[Language] = 'Croatian')
  AND (P1.$node_id <> P3.$node_id);
GO