from db.mysql_db import Database
from data.config import *  # Import all configurations from the config module


db = Database(host=HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)