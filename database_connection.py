import mysql.connector

"""
This is an example code for connecting to the MySQL database hosted at the IP address 102.220.87.178
which has been created for the DSI 2022.

You will need to fill in your team's username and password.

All that this example code does is fetches the available tables in the database. You can write your own
MySQL queries in the cmd variable. You will only be able to perform SELECT and JOIN commands on the database
so it is impossible for you to break anything.

A useful graphical tool for interfacing with MySQL databases is called MySQL Workbench and can be downloaded from

https://dev.mysql.com/downloads/workbench/

You will only need the Client not the Server if asked what components need to be installed..
"""
import mysql
import csv

host = "102.220.87.178"
user = "team_a"
password = "blue_ginger_1523"
database = "weather_data"


def export_table_as_csv(database_list, csv_name):
    opened_csv = open(csv_name, "w")
    historic_data_file = csv.writer(opened_csv)
    historic_data_file.writerows(database_list)
    opened_csv.close()


connection = mysql.connector.connect(host=host, user=user, password=password, database=database, port=3306)
cursor = connection.cursor()

# cmd = """SELECT table_name FROM information_schema.tables WHERE table_schema = "weather_data";"""
# cmd = """SHOW TABLES FROM weather_data;"""


select_data = """SELECT * FROM value_types;"""

cursor.execute(select_data)

return_list = cursor.fetchall()

export_table_as_csv(database_list=return_list, csv_name="value_types.csv")


# print(return_list)

cursor.close()
connection.close()
