import pyodbc

def get_db_connection():
    server = 'DESKTOP-LNOKM7P\SQLEXPRESS'
    bd = 'Reconocimiento_Facial'
    user = 'Reconocimiento'
    password = 'admin'
    
    try:
        connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' +
                                    server + ';DATABASE=' + bd + ';UID=' + user + ';PWD=' + password)
        print('Conexión exitosa')
        return connection
    except Exception as e:
        print(f"Error al intentar conectarse: {e}")
        return None
