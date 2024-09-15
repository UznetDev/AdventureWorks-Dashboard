import logging
import mysql.connector


class Database:
    def __init__(self, host, user, password, database):
        """
        Initialize the Database object with connection parameters.

        Parameters:
        host (str): The hostname of the MySQL server.
        user (str): The username to connect to the MySQL server.
        password (str): The password to connect to the MySQL server.
        database (str): The name of the database to connect to.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.reconnect()


    def reconnect(self):
        """
        Reconnect to the MySQL database. If the connection fails, log the error and attempt to reconnect.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            logging.error(f"Error connecting to database: {err}")
            self.reconnect()
        except Exception as err:
            logging.error(f"Unexpected error: {err}")   


    def create_table_sales_per_day(self):
        """
        Create the 'sales_per_day' table if it does not already exist.
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def insert_table_sales_per_day(self):
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_total_due(self):
        try:
            sql = """SELECT SUM(TotalDue) FROM `Sales_SalesOrderHeader`"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_total_profit(self):
        try:
            sql = """SELECT SUM(sod.LineTotal - p.StandardCost * sod.OrderQty) AS profit
            FROM Sales_SalesOrderDetail sod
            JOIN Production_Product p
            USING(ProductID)"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_count(self):
        try:
            sql = """SELECT COUNT(*) FROM Sales_SalesOrderHeader"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)

    def get_sales_by_category(self, option):
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_territory(self, option):
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_p_region(self, option):
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_p_month(self, option):
        try:
            sql = f"""
                SELECT m.name AS month, SUM({option}) AS v
                FROM Sales_SalesOrderHeader s
                JOIN Sales_SalesOrderDetail sod 
                USING(SalesOrderID)
                JOIN month m 
                ON MONTH(s.DueDate) = m.number
                GROUP BY m.name, m.number
                ORDER BY m.number
                """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_reason_type(self, option):
        try:
            sql = f"""
                SELECT
                    sr.ReasonType,
                    SUM(soh.TotalDue) AS {option}
                FROM
                    Sales_SalesOrderHeader soh
                    INNER JOIN Sales_SalesOrderHeaderSalesReason sohsr ON soh.SalesOrderID = sohsr.SalesOrderID
                    INNER JOIN Sales_SalesReason sr ON sohsr.SalesReasonID = sr.SalesReasonID
                GROUP BY
                    sr.ReasonType;
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_map(self, option):
        try:
            if option == 'TotalDue':
                value_column = 'soh.TotalDue'
            elif option in ['OrderQty', 'NetProfit']:
                value_column = f'sod.{option}'
            else:
                value_column = '0'

            sql = f"""
                SELECT
                    pat.City AS city,
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
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_online_persentage(self, option):
        try:
            if option == 'NetProfit':
                value_column = 'sod.NetProfit'
                where_clause = f'WHERE sod.NetProfit > 0'
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
                SELECT 
                    CASE 
                        WHEN soh.OnlineOrderFlag = 1 THEN 'Online'
                        ELSE 'Offline'
                    END AS Flag,
                    SUM({value_column}) AS TotalValue
                FROM Sales_SalesOrderDetail sod
                JOIN Sales_SalesOrderHeader soh
                ON sod.SalesOrderID = soh.SalesOrderID
                {where_clause}
                GROUP BY Flag;
            """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_locations(self):
        """
        Retrieve a list of available locations.
        """
        try:
            sql = "SELECT DISTINCT Name FROM Sales_SalesTerritory"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            locations = [row[0] for row in result]
            return locations
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_categories(self):
        """
        Retrieve a list of available product categories.
        """
        try:
            sql = "SELECT DISTINCT Name FROM Production_ProductCategory"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            categories = [row[0] for row in result]
            return categories
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_financial_breakdown(self, location=None, category=None):
        """
        Retrieve financial data based on selected location and category using NetProfit.
        """
        try:
            sql = """
            SELECT 
                SUM(sod.LineTotal) AS TotalRevenue,
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
            logging.error(err)
            self.reconnect()
            return None
        except Exception as err:
            logging.error(err)
            return None


    def get_shipmethod_distribution(self, metric='TotalRevenue', location=None, category=None):
        """
        Retrieves the distribution of the specified metric by ShipMethod,
        optionally filtered by location and category.

        Parameters:
        - metric (str): The metric to aggregate ('TotalRevenue' or 'OrderCount').
        - location (str): The name of the location to filter by.
        - category (str): The name of the product category to filter by.

        Returns:
        - List of tuples containing ShipMethod names and aggregated values.
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
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_sales_by_day(self, option, location=None, category=None):
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
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_month(self, option, location=None, category=None):
        try:
            if location is None and category is None:
                try:
                    sql = f"""
                            SELECT m.name AS month, 
                                pc.Name AS product_category, 
                                SUM({option}) AS category_sales
                            FROM Sales_SalesOrderHeader s
                            JOIN Sales_SalesOrderDetail sod 
                            ON s.SalesOrderID = sod.SalesOrderID
                            JOIN Production_Product p 
                            ON sod.ProductID = p.ProductID
                            LEFT JOIN Production_ProductSubcategory psc 
                            ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                            LEFT JOIN Production_ProductCategory pc 
                            ON psc.ProductCategoryID = pc.ProductCategoryID
                            JOIN month m ON MONTH(s.DueDate) = m.number
                            GROUP BY m.name, m.number, pc.Name
                            ORDER BY m.number
                        """
                    self.cursor.execute(sql)
                    return self.cursor.fetchall()
                except mysql.connector.Error as err:
                    logging.error(err)
                    self.reconnect()
                except Exception as err:
                    logging.error(err)
            else:
                try:
                    sql = f"""
                        SELECT m.name AS month, 
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
                        JOIN month m
                        ON MONTH(soh.DueDate) = m.number
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
                    result = self.cursor.fetchall()
                    return result
                except mysql.connector.Error as err:
                    logging.error(err)
                    self.reconnect()
                except Exception as err:
                    logging.error(err)
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_year(self, option, location=None, category=None):
        try:
            if location is None and category is None:
                sql = f"""
                    SELECT
                        YEAR(s.DueDate) AS year,
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
                result = self.cursor.fetchall()
                return result
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)


    def get_sales_by_day_with_category(self,option, location=None):
        """
        Retrieves the sales data by day of the month, broken down by category.
        Optionally filtered by location.
        """
        try:
            sql = f"""
            SELECT DAY(soh.OrderDate) AS Day,
                pc.Name AS Category, 
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
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_sales_by_month_with_category(self,option, location=None):
        try:
            sql = f"""
            SELECT m.name AS month, 
            pc.Name AS Category, 
            SUM({option}) AS TotalSales
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh 
            ON sod.SalesOrderID = soh.SalesOrderID
            JOIN Production_Product p ON sod.ProductID = p.ProductID
            LEFT JOIN Production_ProductSubcategory psc 
            ON p.ProductSubcategoryID = psc.ProductSubcategoryID
            LEFT JOIN Production_ProductCategory pc 
            ON psc.ProductCategoryID = pc.ProductCategoryID
            LEFT JOIN Sales_SalesTerritory st 
            ON soh.TerritoryID = st.TerritoryID
            JOIN month m
            ON MONTH(soh.DueDate) = m.number
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
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []


    def get_sales_by_year_with_category(self, option, location=None):
        """
        Retrieves the sales data by year, broken down by category.
        Optionally filtered by location.
        """
        try:
            sql = f"""
            SELECT YEAR(soh.OrderDate) AS year, 
            pc.Name AS Category, 
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

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " GROUP BY YEAR(soh.OrderDate), pc.Name ORDER BY Year"

            self.cursor.execute(sql, params)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
            return []
        except Exception as err:
            logging.error(err)
            return []



    def fetch_sales_data(self):
        """
        Executes the SQL query to fetch all sales-related data.
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