#script para criar as tabelas iniciais
import Files.passwords as passwords
from Files.interpretador_sql import create_table
from Files.interpretador_sql import connect_to_rds
import mysql.connector
import database_infos
import passwords

user = passwords.user
password = passwords.password
host = passwords.host
database = 'gca'


#criar a tabela de negociações
create_table(passwords.db_user, passwords.db_secret, database_infos.host, database_infos.database ,'negociacoes', ["`Data do Negócio` DATE", "`Tipo de Movimentação` VARCHAR(240)",	"`Mercado` VARCHAR(240)",	
                                                            "`Prazo/Vencimento` VARCHAR(32)", "Instituição VARCHAR(240)", "`Código de Negociação` VARCHAR(240)",	
                                                            "Quantidade FLOAT", "Preço FLOAT",	"Valor FLOAT", "`Arquivo Fonte` VARCHAR(240)", "`cod negociacao` VARCHAR(500)", 'setor VARCHAR(255)', 'UserTag1 VARCHAR(255)', 'UserTag2  VARCHAR(255)'])

cnx = get_cnx('gca', host)

def insert_unique_df_to_table(df, table, cnx):
    # Remove duplicate rows from the dataframe
    # df = df.drop_duplicates()
    
    # Create a cursor for executing the SQL commands
    cursor = cnx.cursor()
    # Iterate over the rows of the dataframe
    for i, row in df.iterrows():
        values = tuple(row)
        query = "INSERT IGNORE INTO {} VALUES {}".format(table, values)
        cursor.execute(query)      
    # Commit the changes
    cnx.commit() 
    # Close the cursor
    cursor.close()

def set_unique_key(conn, cursor, table_name, column_name, constraint_name):
    query = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} UNIQUE({column_name})"
    cursor.execute(query)
    conn.commit()

def remover_negociacoes(cnx):
    confirm = input('Digite "confirma" para deletar as negociacoes: ')
    if confirm == 'confirma':
        query = "DROP TABLE negociacoes"
        cursor = cnx.cursor()
        cursor.execute(query)
        cnx.commit()