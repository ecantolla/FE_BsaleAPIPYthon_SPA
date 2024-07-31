import pyodbc
from Class.ConnectionHandler import ConnectionHandler
from Class.Models.tablas import tablas


def get_datatype(table_name, col_name):
    conn = ConnectionHandler()
    cname_dtype = f"""
    SELECT 
        DATA_TYPE
    FROM 
        INFORMATION_SCHEMA.COLUMNS
    WHERE 
        TABLE_NAME = '{table_name}'
        AND COLUMN_NAME = '{col_name}'
    """
    cursor = conn.executeQuery(cname_dtype)
    datatype = cursor.fetchone()[0]
    conn.closeConnection()
    return datatype

def get_col_dtype(table_name):
    conn = ConnectionHandler()
    cname_dtype = f"""
    SELECT
        COLUMN_NAME,
        DATA_TYPE
    FROM 
        INFORMATION_SCHEMA.COLUMNS
    WHERE 
        TABLE_NAME = '{table_name}';
    """
    cursor = conn.executeQuery(cname_dtype)
    datatype = cursor.fetchall()
    conn.closeConnection()
    return datatype

print(get_col_dtype(tablas['cliente']))
