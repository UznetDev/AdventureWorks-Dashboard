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


    def get_sales_by_tretory(self, option):
        try:
            sql = f"""
            SELECT st.Name AS Territory, SUM({option}) AS TotalSold
            FROM Sales_SalesOrderDetail sod
            JOIN Sales_SalesOrderHeader soh
            USING(SalesOrderID)
            JOIN Sales_SalesTerritory st
            USING(TerritoryID)
            GROUP BY st.Name
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
                SELECT cr.Name AS CountryRegion, SUM({option}) AS TotalSales
                FROM Sales_SalesOrderHeader soh
                JOIN Sales_SalesOrderDetail sod
                USING(SalesOrderID)
                JOIN Sales_Customer c ON soh.CustomerID = c.CustomerID
                JOIN Person_Person pp ON c.PersonID = pp.BusinessEntityID
                JOIN Person_BusinessEntityAddress bea ON pp.BusinessEntityID = bea.BusinessEntityID
                JOIN Person_Address a ON bea.AddressID = a.AddressID
                JOIN Person_StateProvince sp ON a.StateProvinceID = sp.StateProvinceID
                JOIN Person_CountryRegion cr ON sp.CountryRegionCode = cr.CountryRegionCode
                GROUP BY cr.Name
                ORDER BY TotalSales
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


    def get_sales_by_c_month(self, option):
        try:
            sql = f"""
                SELECT m.name AS month, 
                       pc.Name AS product_category, 
                       SUM({option}) AS category_sales
                FROM Sales_SalesOrderHeader s
                JOIN Sales_SalesOrderDetail sod ON s.SalesOrderID = sod.SalesOrderID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
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


    def get_sales_by_c_day(self, option):
        try:
            sql = f"""
                SELECT DAY({option}) AS day, 
                    pc.Name AS product_category, 
                    SUM(Totaldue) AS category_sales
                FROM Sales_SalesOrderHeader s
                JOIN Sales_SalesOrderDetail sod ON s.SalesOrderID = sod.SalesOrderID
                JOIN Production_Product p ON sod.ProductID = p.ProductID
                JOIN Production_ProductSubcategory psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
                JOIN Production_ProductCategory pc ON psc.ProductCategoryID = pc.ProductCategoryID
                GROUP BY day, pc.Name
                ORDER BY day
                """
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(err)
            self.reconnect()
        except Exception as err:
            logging.error(err)