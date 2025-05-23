# data_loader.py
import mysql.connector
import pandas as pd

def load_data(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="pos_system"
    )
    df = pd.read_sql(query, connection)
    connection.close()
    return df
