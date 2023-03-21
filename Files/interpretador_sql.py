import pandas as pd
import os
from datetime import datetime
import mysql.connector
import passwords

def create_table(user, password, host, database, table_name, columns):
    # Connect to the database
    cnx = mysql.connector.connect(
        user=user,
        password=password, 
        host=host,
        database=database
    )
    # Create a cursor object
    cursor = cnx.cursor()
    # Create the table
    table_create_query = "CREATE TABLE {} ({})".format(table_name, ", ".join(columns))
    cursor.execute(table_create_query)
    # Commit the changes
    cnx.commit()
    # Close the cursor and connection
    cursor.close()
    cnx.close()

def get_cnx(database, host):
    # Connect to the database
    cnx = mysql.connector.connect(
        user=passwords.db_user,
        password=passwords.db_secret,
        host=host,
        database=database
    )
    return cnx

def old_insert_unique_df_to_table(cnx, table, df):#recebe o conector do banco, tabela do banco, e arquivo a ser adicionado
    df = df.drop_duplicates()  
    #Create a cursor for executing the SQL commands
    cursor = cnx.cursor()
    # Iterate over the rows of the dataframe
    for i, row in df.iterrows():
        values = tuple(row)
        #query = f"INSERT IGNORE INTO {table} VALUES {values}"
        cursor.execute(query)
    # Commit the changes
    cnx.commit()
    # Close the cursor
    cursor.close()

def insert_to_table(cnx, table, df):#recebe o conector do banco, tabela do banco, e arquivo a ser adicionado
    df = df.drop_duplicates()  
    #Create a cursor for executing the SQL commands
    cursor = cnx.cursor()
    values = [str(tuple(row)) for _, row in df.iterrows()]   
    query = f"INSERT IGNORE INTO {table} VALUES {','.join(values)}"
    cursor.execute(query)
    cnx.commit() 
    cursor.close()

def get_table_as_dataframe(cnx, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, cnx)
    return df


# Example usage
if __name__ == "__main__":
    import database_infos
    cnx = get_cnx(
        database=database_infos.database,
        host=database_infos.host,
        user=passwords.user,
        password=passwords.secret
    )

