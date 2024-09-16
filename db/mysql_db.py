import logging
import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        """
        Initializes the Database object with connection parameters and connects to the MySQL database.

        Parameters:
        host (str): The hostname of the MySQL server.
        user (str): The username for connecting to the MySQL server.
        password (str): The password for connecting to the MySQL server.
        database (str): The name of the database to connect to.

        Raises:
        mysql.connector.Error: If there is an error connecting to the MySQL database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.reconnect()


    def reconnect(self,err=None, retries=5):
        """
        Reconnects to the MySQL database if the connection is lost. This function attempts to reconnect multiple times in case of failure.

        Parameters:
        retries (int, optional): Number of attempts to reconnect. Defaults to 5.

        Raises:
        mysql.connector.Error: If unable to connect after the specified retries.
        """
        if err:
            self.reconnect(err=err)
            print(err)
        logging.warning('reconnecting MYSQL')
        attempt = 0
        while attempt < retries:
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=True
                )
                self.cursor = self.connection.cursor()
                break
            except mysql.connector.Error as err:
                logging.error(f"Error connecting to database: {err}")
                attempt += 1
                if attempt == retries:
                    raise
            except Exception as err:
                logging.error(f"Unexpected error: {err}")
                attempt += 1
                if attempt == retries:
                    raise


    def create_table_sales_per_day(self):
        """
        Creates the 'sales_per_day' table if it doesn't exist in the database.

        The table has the following schema:
        - day (INT): Represents the day of the month.
        - count (INT): Represents the number of sales on that day.

        Raises:
        mysql.connector.Error: If there is an error creating the table.
        """
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS `sales_per_day` (
                day INT NOT NULL UNIQUE,
                count INT
            )
            """
            self.cursor.execute(sql)
            self.connection.commit()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            return []


    def insert_table_sales_per_day(self):
        """
        Inserts sales data into the 'sales_per_day' table, aggregating sales by day.

        Data is inserted only if the table is currently empty. The aggregation is done by 
        summing up the 'OrderQty' from the Sales_SalesOrderDetail table, grouped by the day.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = """SELECT * FROM `sales_per_day`"""
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if not result:
                sql = """
                INSERT INTO `sales_per_day`(`day`, `count`)
                SELECT DAY(ssoh.OrderDate) AS day, 
                    SUM(ssod.OrderQty) AS count 
                FROM `Sales_SalesOrderHeader` ssoh 
                JOIN `Sales_SalesOrderDetail` ssod 
                USING(SalesOrderID)
                GROUP BY DAY(ssoh.OrderDate)
                ORDER BY DAY(ssoh.OrderDate);
                """
                self.cursor.execute(sql)
                self.connection.commit()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_total_due(self):
        """
        Fetches the total 'TotalDue' value from the 'Sales_SalesOrderHeader' table.

        Returns:
        float: The sum of all TotalDue values in the database.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = """SELECT SUM(TotalDue) FROM `Sales_SalesOrderHeader`"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_total_profit(self):
        """
        Fetches the total profit by calculating the difference between 'LineTotal' and 
        the cost of products from the 'Sales_SalesOrderDetail' and 'Production_Product' tables.

        Returns:
        float: The total calculated profit.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = """
            SELECT SUM(sod.LineTotal - p.StandardCost * sod.OrderQty) AS profit
            FROM Sales_SalesOrderDetail sod
            JOIN Production_Product p
            USING(ProductID)
            """
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logging.error(f"MySQL Error: {err}")
            self.reconnect()
            return []
        except Exception as err:
            logging.error(f"Unexpected Error: {err}")
            self.reconnect()
            return []

                

    def get_sales_count(self):
        """
        Fetches the total number of sales records from the 'Sales_SalesOrderHeader' table.

        Returns:
        int: The count of sales orders in the database.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = """SELECT COUNT(*) FROM Sales_SalesOrderHeader"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_category(self, option):
        """
        Fetches sales data grouped by product category, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').

        Returns:
        list: A list of tuples containing category name and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
                SELECT pc.Name AS CategoryName, SUM({option}) AS TotalSold
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader as soh
                USING(SalesOrderID)
                JOIN Production_Product p 
                USING(ProductID)
                JOIN Production_ProductSubcategory psc
                USING(ProductSubcategoryID)
                JOIN Production_ProductCategory pc
                USING(ProductCategoryID)
                GROUP BY pc.Name
                ORDER BY TotalSold DESC
                """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_territory(self, option):
        """
        Fetches sales data grouped by territory and product category, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').

        Returns:
        list: A list of tuples containing territory, product category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
                SELECT st.Name AS Territory, 
                    pc.Name AS ProductCategory, 
                    SUM({option}) AS TotalSold
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                GROUP BY st.Name, pc.Name
                ORDER BY TotalSold DESC
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_p_region(self, option):
        """
        Fetches sales data grouped by country region and product category, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').

        Returns:
        list: A list of tuples containing country region, product category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
                SELECT cr.Name AS CountryRegion, 
                    pc.Name AS ProductCategory, 
                    SUM({option}) AS TotalSales
                FROM Sales_SalesOrderHeader soh
                JOIN Sales_SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                JOIN Sales_Customer c ON soh.CustomerID = c.CustomerID
                JOIN Person_Person pp ON c.PersonID = pp.BusinessEntityID
                JOIN Person_BusinessEntityAddress bea ON pp.BusinessEntityID = bea.BusinessEntityID
                JOIN Person_Address a ON bea.AddressID = a.AddressID
                JOIN Person_StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
                JOIN Person_CountryRegion cr ON sp.CountryRegionCode = cr.CountryRegionCode
                GROUP BY cr.Name, pc.Name
                ORDER BY TotalSales DESC
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []
    

    def get_sales_by_month(self, option, location=None, category=None):
        """
        Fetches sales data grouped by month and aggregates based on the specified option.
        Optionally, the results can be filtered by location and product category.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.
        category (str, optional): The product category to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing month, product category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if location is None and category is None:
                sql = f"""
                    SELECT m.name AS month, 
                           pc.Name AS product_category, 
                           SUM({option}) AS category_sales
                    FROM Sales_SalesOrderHeader s
                    JOIN Sales_SalesOrderDetail sod ON s.SalesOrderID = sod.SalesOrderID
                    JOIN Production_Product p ON sod.ProductID = p.ProductID
                    LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                    JOIN month m ON MONTH(s.DueDate) = m.number
                    GROUP BY m.name, m.number, pc.Name
                    ORDER BY m.number
                """
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            else:
                sql = f"""
                    SELECT m.name AS month, SUM({option}) AS TotalSales
                    FROM Sales_SalesOrderDetail sod
                    JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                    JOIN Production_Product p ON sod.ProductID = p.ProductID
                    LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                    LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                    JOIN month m ON MONTH(soh.DueDate) = m.number
                """
                conditions = []
                params = []

                if location and location != 'All':
                    conditions.append("st.Name = %s")
                    params.append(location)

                if category and category != 'All':
                    conditions.append("pc.Name = %s")
                    params.append(category)

                if conditions:
                    sql += " WHERE " + " AND ".join(conditions)

                sql += " GROUP BY month"

                self.cursor.execute(sql, params)
                return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_year(self, option, location=None, category=None):
        """
        Fetches sales data grouped by year and aggregates based on the specified option.
        Optionally, the results can be filtered by location and product category.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.
        category (str, optional): The product category to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing year, product category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if location is None and category is None:
                sql = f"""
                    SELECT YEAR(s.DueDate) AS year,
                           pc.Name AS product_category, 
                           SUM({option}) AS category_sales
                    FROM Sales_SalesOrderHeader s
                    JOIN Sales_SalesOrderDetail sod ON s.SalesOrderID = sod.SalesOrderID
                    JOIN Production_Product p ON sod.ProductID = p.ProductID
                    JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                    GROUP BY year, product_category
                    ORDER BY year
                """
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            else:
                sql = f"""
                    SELECT YEAR(soh.OrderDate) AS Year, 
                           SUM({option}) AS TotalSales
                    FROM Sales_SalesOrderDetail sod
                    JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                    JOIN Production_Product p ON sod.ProductID = p.ProductID
                    LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                    LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                """
                conditions = []
                params = []

                if location and location != 'All':
                    conditions.append("st.Name = %s")
                    params.append(location)

                if category and category != 'All':
                    conditions.append("pc.Name = %s")
                    params.append(category)

                if conditions:
                    sql += " WHERE " + " AND ".join(conditions)

                sql += " GROUP BY YEAR(soh.OrderDate) ORDER BY Year"

                self.cursor.execute(sql, params)
                return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_reason_type(self, option):
        """
        Fetches sales data grouped by sales reason type and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue').

        Returns:
        list: A list of tuples containing the sales reason type and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
                SELECT sr.ReasonType, SUM(soh.TotalDue) AS {option}
                FROM Sales_SalesOrderHeader soh
                JOIN Sales_SalesOrderHeaderSalesReason sohsr ON soh.SalesOrderID = sohsr.SalesOrderID
                JOIN Sales_SalesReason sr ON sohsr.SalesReasonID = sr.SalesReasonID
                GROUP BY sr.ReasonType
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_map(self, option):
        """
        Fetches sales data along with geographic information, aggregating the data based on the specified option.
        The query retrieves city, latitude, longitude, and the aggregated value.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty', 'NetProfit').

        Returns:
        list: A list of tuples containing city, longitude, latitude, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if option == 'TotalDue':
                value_column = 'soh.TotalDue'
            elif option in ['OrderQty', 'NetProfit']:
                value_column = f'sod.{option}'
            else:
                value_column = '0'

            sql = f"""
                SELECT pat.City AS city,
                       ST_X(pat.SpatialLocation) AS Longitude, 
                       ST_Y(pat.SpatialLocation) AS Latitude,
                       SUM({value_column}) AS value
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                JOIN Person_BusinessEntityAddress pbea ON pbea.BusinessEntityID = soh.SalesPersonID
                JOIN Person_Address pat ON pat.AddressID = pbea.AddressID
                GROUP BY city, Longitude, Latitude
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_online_percentage(self, option):
        """
        Fetches the percentage of online versus offline orders and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty', 'NetProfit').

        Returns:
        list: A list of tuples containing the order type ('Online' or 'Offline') and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if option == 'NetProfit':
                value_column = 'sod.NetProfit'
                where_clause = 'WHERE sod.NetProfit > 0'
            elif option == 'TotalDue':
                value_column = 'soh.TotalDue'
                where_clause = ''
            elif option == 'OrderQty':
                value_column = 'sod.OrderQty'
                where_clause = ''
            else:
                value_column = '0'
                where_clause = ''

            sql = f"""
                SELECT CASE 
                        WHEN soh.OnlineOrderFlag = 1 THEN 'Online'
                        ELSE 'Offline'
                       END AS Flag,
                       SUM({value_column}) AS TotalValue
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                {where_clause}
                GROUP BY Flag
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_locations(self):
        """
        Fetches a list of distinct locations (territories) from the database.

        Returns:
        list: A list of unique location names.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = "SELECT DISTINCT Name FROM Sales_SalesTerritory"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            locations = [row[0] for row in result]
            return locations
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_categories(self):
        """
        Fetches a list of distinct product categories from the database.

        Returns:
        list: A list of unique product category names.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = "SELECT DISTINCT Name FROM Production_ProductCategory"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            categories = [row[0] for row in result]
            return categories
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_financial_breakdown(self, location=None, category=None):
        """
        Fetches financial data based on selected location and category, calculating total revenue, production cost,
        delivery cost, and net profit.

        Parameters:
        location (str, optional): The sales territory to filter by. Defaults to None.
        category (str, optional): The product category to filter by. Defaults to None.

        Returns:
        tuple: A tuple containing total revenue, production cost, delivery cost, and net profit.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = """
            SELECT SUM(sod.LineTotal) AS TotalRevenue,
                   SUM(sod.OrderQty * p.StandardCost) AS ProductionCost,
                   SUM(soh.Freight / soh.SubTotal * sod.LineTotal) AS DeliveryCost,
                   SUM(sod.NetProfit) AS NetProfit
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
            JOIN Production_Product p ON sod.ProductID = p.ProductID
            LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
            """
            conditions = []
            params = []

            if location and location != 'All':
                conditions.append("st.Name = %s")
                params.append(location)

            if category and category != 'All':
                conditions.append("pc.Name = %s")
                params.append(category)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_shipmethod_distribution(self, metric='TotalRevenue', location=None, category=None):
        """
        Retrieves the distribution of the specified metric by ShipMethod,
        optionally filtered by location and category.

        Parameters:
        - metric (str): The metric to aggregate ('TotalRevenue' or 'OrderCount').
        - location (str, optional): The name of the location to filter by. Defaults to None.
        - category (str, optional): The name of the product category to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing ShipMethod names and aggregated values for the specified metric.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if metric == 'TotalRevenue':
                sql = """
                SELECT sm.Name AS ShipMethod, SUM(sod.LineTotal) AS TotalRevenue
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                JOIN Purchasing_ShipMethod sm ON soh.ShipMethodID = sm.ShipMethodID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                """
                order_by_column = "TotalRevenue"
            elif metric == 'OrderCount':
                sql = """
                SELECT sm.Name AS ShipMethod, COUNT(*) AS OrderCount
                FROM Sales_SalesOrderHeader soh
                JOIN Purchasing_ShipMethod sm ON soh.ShipMethodID = sm.ShipMethodID
                JOIN Sales_SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                """
                order_by_column = "OrderCount"
            else:
                sql = """
                SELECT sm.Name AS ShipMethod, SUM(sod.LineTotal) AS TotalRevenue
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
                JOIN Purchasing_ShipMethod sm ON soh.ShipMethodID = sm.ShipMethodID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
                """
                order_by_column = "TotalRevenue"

            conditions = []
            params = []

            if location and location != 'All':
                conditions.append("st.Name = %s")
                params.append(location)

            if category and category != 'All':
                conditions.append("pc.Name = %s")
                params.append(category)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += f" GROUP BY sm.Name ORDER BY {order_by_column} DESC;"

            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_day(self, option, location=None, category=None):
        """
        Fetches sales data grouped by day of the month, optionally filtered by location and category,
        and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.
        category (str, optional): The product category to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing the day, product category (if applicable), and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            if location is None and category is None:
                sql = f"""
                    SELECT DAY(DueDate) AS day, 
                           pc.Name AS product_category, 
                           SUM({option}) AS category_sales
                    FROM Sales_SalesOrderDetail sod
                    JOIN Sales_SalesOrderHeader soh 
                    ON sod.SalesOrderID = soh.SalesOrderID
                    JOIN Production_Product p 
                    ON sod.ProductID = p.ProductID
                    LEFT JOIN Production_ProductSubcategory psc 
                    ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    LEFT JOIN Production_ProductCategory pc 
                    ON psc.ProductCategoryID = pc.ProductCategoryID
                    GROUP BY day, pc.Name
                    ORDER BY day
                """
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            else:
                sql = f"""
                    SELECT DAY(soh.OrderDate) AS Day, 
                           SUM({option}) AS TotalSales
                    FROM Sales_SalesOrderDetail sod
                    JOIN Sales_SalesOrderHeader soh 
                    ON sod.SalesOrderID = soh.SalesOrderID
                    JOIN Production_Product p 
                    ON sod.ProductID = p.ProductID
                    LEFT JOIN Production_ProductSubcategory psc 
                    ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                    LEFT JOIN Production_ProductCategory pc 
                    ON psc.ProductCategoryID = pc.ProductCategoryID
                    LEFT JOIN Sales_SalesTerritory st 
                    ON soh.TerritoryID = st.TerritoryID
                """
                conditions = []
                params = []

                if location and location != 'All':
                    conditions.append("st.Name = %s")
                    params.append(location)

                if category and category != 'All':
                    conditions.append("pc.Name = %s")
                    params.append(category)

                if conditions:
                    sql += " WHERE " + " AND ".join(conditions)

                sql += " GROUP BY DAY(soh.OrderDate) ORDER BY Day"

                self.cursor.execute(sql, params)
                return self.cursor.fetchall()
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_day_with_category(self, option, location=None):
        """
        Fetches sales data grouped by day of the month, broken down by category,
        optionally filtered by location, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing the day, category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
            SELECT DAY(soh.OrderDate) AS Day,
                   pc.Name AS Category, 
                   SUM({option}) AS TotalSales
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
            JOIN Production_Product p ON sod.ProductID = p.ProductID
            LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
            """
            conditions = []
            params = []

            if location and location != 'All':
                conditions.append("st.Name = %s")
                params.append(location)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " GROUP BY DAY(soh.OrderDate), pc.Name ORDER BY Day"

            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_month_with_category(self, option, location=None):
        """
        Fetches sales data grouped by month, broken down by category,
        optionally filtered by location, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing the month, category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
            SELECT m.name AS month, 
                   pc.Name AS Category, 
                   SUM({option}) AS TotalSales
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
            JOIN Production_Product p ON sod.ProductID = p.ProductID
            LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
            JOIN month m ON MONTH(soh.DueDate) = m.number
            """
            conditions = []
            params = []

            if location and location != 'All':
                conditions.append("st.Name = %s")
                params.append(location)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += """ GROUP BY month, pc.Name ORDER BY (
            SELECT number 
            FROM month AS m2
            WHERE m2.name=month
            )"""

            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_sales_by_year_with_category(self, option, location=None):
        """
        Fetches sales data grouped by year, broken down by category,
        optionally filtered by location, and aggregates based on the specified option.

        Parameters:
        option (str): The metric to aggregate (e.g., 'TotalDue', 'OrderQty').
        location (str, optional): The sales territory to filter by. Defaults to None.

        Returns:
        list: A list of tuples containing the year, category, and the aggregated value for the specified option.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        try:
            sql = f"""
            SELECT YEAR(soh.OrderDate) AS year, 
                   pc.Name AS Category, 
                   SUM({option}) AS TotalSales
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh ON sod.SalesOrderID = soh.SalesOrderID
            JOIN Production_Product p ON sod.ProductID = p.ProductID
            LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
            """
            conditions = []
            params = []

            if location and location != 'All':
                conditions.append("st.Name = %s")
                params.append(location)

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " GROUP BY YEAR(soh.OrderDate), pc.Name ORDER BY Year"

            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            self.reconnect(err=err)
            print(err)
            self.reconnect(err=err)
            return []
        except Exception as err:
            self.reconnect(err=err)
            print(err)
            return []


    def get_all_data(self):
        """
        Fetches all sales-related data from the 'Sales_SalesOrderHeader' and 'Sales_SalesOrderDetail' tables.
        This includes details like order date, product, customer, and total amount.

        Returns:
        list: A list of tuples containing all sales data including order information, product details, and customer details.

        Raises:
        mysql.connector.Error: If there is an error executing the query.
        """
        query = """
        SELECT
            soh.SalesOrderID,
            soh.OrderDate,
            soh.DueDate,
            soh.ShipDate,
            soh.Status,
            soh.OnlineOrderFlag,
            soh.SalesOrderNumber,
            soh.PurchaseOrderNumber,
            soh.SubTotal,
            soh.TaxAmt,
            soh.Freight,
            soh.TotalDue,
            soh.Comment,
            sod.ProductID,
            sod.OrderQty,
            sod.UnitPrice,
            sod.LineTotal,
            sod.UnitPriceDiscount,
            p.Name AS ProductName,
            p.ProductNumber,
            p.Color,
            p.StandardCost,
            p.ListPrice,
            psc.Name AS SubcategoryName,
            pc.Name AS CategoryName,
            st.Name AS TerritoryName,
            sm.Name AS ShipMethodName,
            c.CustomerID,
            c.AccountNumber,
            pa.AddressLine1,
            pa.City,
            pa.StateProvinceID,
            pa.PostalCode
        FROM Sales_SalesOrderHeader soh
        JOIN Sales_SalesOrderDetail sod ON soh.SalesOrderID = sod.SalesOrderID
        JOIN Production_Product p ON sod.ProductID = p.ProductID
        LEFT JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
        LEFT JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
        LEFT JOIN Sales_SalesTerritory st ON soh.TerritoryID = st.TerritoryID
        LEFT JOIN Purchasing_ShipMethod sm ON soh.ShipMethodID = sm.ShipMethodID
        LEFT JOIN Sales_Customer c ON soh.CustomerID = c.CustomerID
        LEFT JOIN Person_Address pa ON c.PersonID = pa.AddressID;
        """
        
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(f"MySQL error: {err}")
            return []
