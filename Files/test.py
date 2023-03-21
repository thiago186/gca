import pandas as pd
import sqlite3
#script para criar as tabelas iniciais
import passwords
from interpretador_sql import create_table
import mysql.connector
import database_infos
import passwords as passwords
import database_infos as database
from interpretador_sql import get_cnx
from tkinter import filedialog
#print('teste github')
user = passwords.db_user
password = passwords.db_secret
host = database.host
database = 'gca'

cnx = get_cnx('gca', host)
# Set the file path to the Excel file
file_path = filedialog.askopenfilename()

# Read the Excel file into a Pandas DataFrame
df = pd.read_excel(file_path)

# Set up a connection to a SQLite database


# Write the DataFrame to a SQL table
df.to_sql('table_name', cnx, if_exists='replace', index=False)

# Close the database connection
conn.close()