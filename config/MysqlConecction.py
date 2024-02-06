import mysql.connector
import pandas as pd

# Datos de conexión a la base de datos MySQL


def ConecctionDatabase(consulta,database,user,password):
# Consulta SQL que deseas ejecutar
    host = '#'
    #database = '#'
    port= '3306'
    #user = '#'
    #password = '#'

# Realizar la conexión a la base de datos
    connection = mysql.connector.connect(host=host,port=port, database=database, user=user, password=password)

# Ejecutar la consulta y obtener los resultados en un DataFrame
    if connection.is_connected():
        df = pd.read_sql_query(consulta, connection)
        connection.close()
        return df
    else:
        return "Error con la consulta"

    


