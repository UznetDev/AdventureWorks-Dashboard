import datetime
from environs import Env


# Initialize the Env object to read environment variables
env = Env()
env.read_env()

HOST = env.str('HOST')  # The host for the database
MYSQL_USER = env.str('MYSQL_USER')  # The MySQL database user
MYSQL_PASSWORD = env.str('MYSQL_PASSWORD')  # The MySQL database password
MYSQL_DATABASE = env.str('MYSQL_DATABASE')  # The MySQL database name

date_day_month = (datetime.datetime.date(datetime.datetime.now()))
time_hour_minute_second = f"{datas.hour}:{datas.minute}:{datas.second}"