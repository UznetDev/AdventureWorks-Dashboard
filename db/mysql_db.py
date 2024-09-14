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