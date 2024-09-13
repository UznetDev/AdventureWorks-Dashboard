# SQL Server 2017 Graph Database

SQL Server has always provided tools to manage hierarchies and relationships, facilitating query execution on hierarchical data, but sometimes relationships can become complex. Think about many-to-many relationships, relational databases don't have a native solution for many-to-many associations. A common approach to realize many-to-many associations is to introduce a table that holds such relationships.

SQL Server 2017, thanks to Graph Database, can express certain kinds of queries more easily than a relational database by transforming complex relationships into graphs.

These demos, based on [WideWorldImporters](https://github.com/Microsoft/sql-server-samples/tree/master/samples/databases/wide-world-importers) sample database, are related to the session that [Sergio Govoni](https://mvp.microsoft.com/it-it/PublicProfile/4029181?fullName=Sergio%20Govoni) has done at the PASS SQL Saturday 675 in Parma (Italy).

For those who don't already know the [SQL Saturday](http://www.sqlsaturday.com) events: Since 2007, the PASS SQL Saturday program provides users around the world the opportunity to organize free training sessions on SQL Server and related technologies. SQL Saturday is an event sponsored by PASS and therefore offers excellent opportunities for training, professional exchange and networking. You can find all details in this page: [About PASS SQL Saturday](http://www.sqlsaturday.com/about.aspx).


### Contents

[About this sample](#about-this-sample)<br/>
[Before you begin](#before-you-begin)<br/>
[Run this sample](#run-this-sample)<br/>
[Disclaimers](#disclaimers)<br/>
[Related links](#related-links)<br/>

<a name=about-this-sample></a>

## About this sample

1. **Applies to:**
	- Azure SQL Database v12 (or higher)
	- SQL Server 2017 (or higher)
2. **Demos:**
	- Build and populating nodes and edges tables
        - The new MATCH function
	- Build a recommendation system for sales offers
3. **Workload:**  Queries executed on [WideWorldImporters](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)
4. **Programming Language:** T-SQL
5. **Author:** [Sergio Govoni](https://mvp.microsoft.com/it-it/PublicProfile/4029181?fullName=Sergio%20Govoni)

<a name=before-you-begin></a>

## Before you begin

To run these demos, you need the following prerequisites.

**Account and Software prerequisites:**

1. Either
	- Azure SQL Database v12 (or higher)
	- SQL Server 2017 (or higher)
2. SQL Server Management Studio 17.x (or higher)

**Azure prerequisites:**

1. An Azure subscription. If you don't already have an Azure subscription, you can get one for free here: [get Azure free trial](https://azure.microsoft.com/en-us/free/)

2. When your Azure subscription is ready to use, you have to create an Azure SQL Database, to do that, you must have completed the first three steps explained in [Design your first Azure SQL database](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-design-first-database)

<a name=run-this-sample></a>

## Run this sample

### Setup

#### Azure SQL Database Setup

1. Download the **WideWorldImporters-Standard.bacpac** from the WideWorldImporters database [page](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)

2. Import the **WideWorldImporters-Standard.bacpac** bacpac file to your Azure subscription. This [article](https://www.sqlshack.com/import-sample-bacpac-file-azure-sql-database/) on SQL Shack explains how to import WideWorldImporters database to an Azure SQL Database, anyway, the instructions are valid for any bacpac file

3. Launch SQL Server Management Studio and connect to the newly created WideWorldImporters-Standard database

#### SQL Server Setup

1. Download **WideWorldImporters-Full.bak** from the WideWorldImporters database [page](https://github.com/Microsoft/sql-server-samples/releases/tag/wide-world-importers-v1.0)

2. Launch SQL Server Management Studio, connect to your SQL Server instance (2017) and restore **WideWorldImporters-Full.bak**. For further information about how to restore a database backup using SQL Server Management Studio, you can refer to this article: [Restore a Database Backup Using SSMS](https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/restore-a-database-backup-using-ssms). Once you have restored the WideWorldImporters database, you can connect it using the **USE** command like this:

```SQL
USE [WideWorldImporters]
```

The purpose of the file [before-you-begin.sql](./before-you-begin.sql) is to connect the database WideWorldImporters and create two new schema: **Edges** and **Nodes**.


### Create and populate graph objects

The first demo consists of creating graph objects such as Nodes and Edges, this is the purpose of the file [demo1-create-and-populate-nodes-and-edges.sql](./demo1-create-and-populate-nodes-and-edges.sql). Let's start with the Node table named **Nodes.Person**. A node table represents an entity in a Graph DB, every time a node is created, in addition to the user defined columns, SQL Server Engine will create an implicit column named **$node_id** that uniquely identifies a given node in the database, it contains a combination of the **object_id** of the node and an internally bigint stored in an hidden column named **graph_id**.

The following picture shows the CREATE statement with the new DDL extension **AS NODE**, this extension tells the engine that we want to create a Node table.

![Picture 1](../../../../media/demos/sql-graph/Create%20a%20Node%20Table.png)

Now, it's time to create the Edge table named **Edges.Friends**. Every Edge represents a relationship in a graph, it may or may not have any user defined attributes, Edges are always directed and connected with two nodes. In the first release of SQL Graph, constraints are not available on the Edge table, so an Edge table can connect any two nodes on the graph. Every time an Edge table is created, in addition to the user defined columns, the Engine will create three implicit columns:

1. **$edge_id** is a combination of the **object_id** of the Edge and an internally bigint stored in an hidden column named **graph_id**

2. **$from_id** stores the **$node_id** of the node where the Edge starts from

3. **$to_id** stores the **$node_id** of the node at which the Edge ends

The following picture shows the CREATE statement with the new DDL extension **AS EDGE**, this extension tells the engine that we want to create an Edge table.

![Picture 2](../../../../media/demos/sql-graph/Create%20an%20Edge%20Table.png)

The node **Nodes.Person** and the edge **Edges.Friends** are populated starting from the table **Application.People** of WideWorldImporters DB.

### The first look to the MATCH clause

The second demo allows you to do a first look to the MATCH clause used to perform some query on Nodes and Edges we have just created (in the first demo).

The new T-SQL MATCH function allows you to specify the search pattern for a graph schema, it can be used only with graph Node and Edge tables in SELECT statements as a part of the WHERE clause. Based on the node **Nodes.Person** and the edge **Edges.Friends**, the file [demo2-using-the-match-clause.sql](./demo2-using-the-match-clause.sql) contains the following sample queries:

1. List of all people who speak Finnish with friends (Pattern: Node > Relationship > Node)

2. List of the top 5 people who have friends that speak Greek in the first and second connections

3. People who have common friends that speak Croatian

The search pattern, provided in the MATCH function, goes through one node to another by an edge, in the direction provided by the arrow. Edge names or aliases are provided inside parenthesis. Node names or aliases appear at the two ends of the arrow.


### Build a sample recommendation system using SQL Graph

Suppose we have a customer (from the table Sales.Customers) connected to our e-commerce, and this customer is looking for the product (of the table Warehouse.StockItems) "USB food flash drive - pizza slice" or they have just bought that product. Our goal is finding similar products to the one they are looking at, based on the behavior of other customers.

The following picture shows a possible scenario for our sales recommendation system.

![Picture 3](../../../../media/demos/sql-graph/Sales%20Recommendation%20Scenario.png)

This is the algorithm:

1. Identify the customer and the product they are purchasing

2. Identify the other customers who have purchased the same they are looking for

3. Find the other products that customers, at step two, have purchased

4. Recommend to the current customer the top items from the previous step, ordered by the number of times they were purchased

The following picture shows the graphical representation of the algorithm.

![Picture 4](../../../../media/demos/sql-graph/Sales%20Recommendation%20System.png)

The file [demo3-create-and-populate-nodes-and-edges.sql](./demo3-create-and-populate-nodes-and-edges.sql) contains the statements to create and populate the nodes **Nodes.Customers**, **Nodes.StockItems** and the edge **Edges.Bought** starting from the tables of WideWorldImporters DB.

How can Graph Database help us to implement this algorithm?

MATCH clause can express certain kinds of queries more easily than relational JOINs. If we use the counts to prioritize the recommendations that is the simplest possible algorithm for a recommendation service, in reality more complex filters are applied on top, for example text analysis of the product reviews to arrive at similar measures.

The file [demo3-recommendation-system-for-sales.sql](./demo3-recommendation-system-for-sales.sql) contains the query that is able to extract top 5 products that are recommended for "USB food flash drive - pizza slice" using the MATCH clause.

The last query of the file [demo3-recommendation-system-for-sales.sql](./demo3-recommendation-system-for-sales.sql) shows  the implementation of the algorithm in the relational database using JOINs.. so you know how many lines of code you would have written prior to SQL Graph Database.

<a name=disclaimers></a>

## Disclaimers

The code included in this sample is not intended to be a set of best practices on how to build scalable enterprise grade applications. This is beyond the scope of this quick start sample.

<a name=related-links></a>

## Related Links

For more information about Graph DB in SQL Server 2017, see these articles:

1. [Graph processing with SQL Server and Azure SQL Database](https://docs.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-overview)

2. [SQL Graph Architecture](https://docs.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-architecture)

3. [Arvind Shyamsundar's Blog](https://blogs.msdn.microsoft.com/arvindsh/)
