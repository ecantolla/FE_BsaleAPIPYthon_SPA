import pyodbc

host = 'localhost'
database = 'BSALE_FARMACIA'
passwd = 'Ucbh2016'
user = 'wsilva'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={host};DATABASE={database};UID={user};PWD={passwd};Encrypt=no;TrustServerCertificate=yes'
conn = pyodbc.connect(connectionString)
cursor = conn.cursor()
res = cursor.execute('select * from dbo.ATRIBUTO')
records = cursor.fetchall()
print(records)
