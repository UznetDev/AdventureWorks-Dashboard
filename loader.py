from db.mysql_db import Database
from data.config import HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


db = Database(host=HOST, 
              user=MYSQL_USER, 
              password=MYSQL_PASSWORD, 
              database=MYSQL_DATABASE)
