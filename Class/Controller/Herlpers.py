from Class.ConnectionHandler import ConnectionHandler


def get_col_dtype(table_name):
    conn = ConnectionHandler()
    conn.connect()
    cname_dtype = f"""
    SELECT
        COLUMN_NAME,
        DATA_TYPE
    FROM 
        INFORMATION_SCHEMA.COLUMNS
    WHERE 
        TABLE_NAME = '{table_name}';
    """
    col_dtype = conn.executeQuery(cname_dtype, 'select')
    return col_dtype


def format_record(datas, cols, dtypes):
    new_data = {k: v for k, v in datas.items() if k in cols}

    for col, dtype in zip(cols, dtypes):
        if new_data[col] is not None:
            if new_data[col] != '':
                if dtype == 'nvarchar':
                    new_data[col] = str(new_data[col])
                elif dtype == 'int':
                    new_data[col] = int(new_data[col])
                elif dtype == 'float':
                    new_data[col] = float(new_data[col])
                elif new_data[col] is dict:
                    new_data[col] = new_data[col]['href']
            else:
                if dtype == 'int':
                    new_data[col] = None
                elif dtype == 'float':
                    new_data[col] = 0.0

    return new_data
