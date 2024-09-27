import cx_Oracle
from Models.DatabaseModel import get_db_connection
from datetime import datetime

def get_employee_by_credentials(username, password):
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = connection.cursor()
    
    query = """
    SELECT u.Id_empleado, e.nombre, e.apellido 
    FROM Usuarios u
    JOIN Empleados e ON u.Id_empleado = e.Id_empleado
    WHERE u.nombre_usuario = ? AND u.contraseña = ?
    """
    
    cursor.execute(query, (username, password))
    employee = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return employee

def get_employee_profile(employee_id):
    try:
        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        # Consulta para obtener el correo y teléfono del empleado
        query = "SELECT Email, telefono FROM Empleados WHERE Id_empleado = ?"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        if result:
            email, telefono = result
            return email, telefono
        else:
            return None, None

    except Exception as e:
        print("Error al obtener los datos del empleado:", e)
        return None, None

    finally:
        connection.close()

def update_employee_profile(employee_id, new_email, new_phone):
    try:
        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        # Consulta para actualizar el correo y el teléfono del empleado
        query = "UPDATE Empleados SET Email = ?, telefono = ? WHERE Id_empleado = ?"
        cursor.execute(query, (new_email, new_phone, employee_id))
        connection.commit()

        return True  # Si todo fue bien, retornamos True
    except Exception as e:
        print("Error al actualizar los datos del empleado:", e)
        return False  # Si algo salió mal, retornamos False
    finally:
        connection.close()


def get_work_hours(employee_id, start_date=None, end_date=None):
    # Conectar a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Definir la consulta SQL y los parámetros
    if start_date and end_date:
        # Asegúrate de que las fechas sean del tipo correcto y en el formato adecuado
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        query = """
        SELECT fecha, horas_totales 
        FROM horas_trabajadas 
        WHERE id_empleado = ? 
        AND fecha BETWEEN ? AND ?
        """
        params = (employee_id, start_date_str, end_date_str)
    else:
        # Obtener el mes y año actual
        current_month = datetime.now().month
        current_year = datetime.now().year

        query = """
        SELECT fecha, horas_totales 
        FROM horas_trabajadas 
        WHERE id_empleado = ? 
        AND MONTH(fecha) = ? 
        AND YEAR(fecha) = ?
        """
        params = (employee_id, current_month, current_year)

    # Ejecutar la consulta con los parámetros
    cursor.execute(query, params)

    # Recoger los resultados
    data = cursor.fetchall()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    # Convertir los resultados a una lista de listas
    formatted_data = []
    for record in data:
        fecha = record[0]  # Suponemos que es la columna de fecha
        if isinstance(fecha, str):
            # Si fecha es una cadena, convertirla a datetime
            fecha = datetime.strptime(fecha, "%Y-%m-%d")  # Ajusta el formato según tu base de datos
        formatted_data.append([fecha.strftime("%d-%m-%Y"), f"{record[1]} horas"])

    return formatted_data