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
    connection = None
    cursor = None
    try:
        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        # Consulta SQL para obtener las horas trabajadas de un empleado
        query = """
            SELECT TO_CHAR(fecha, 'DD-MM-YYYY') AS dia, horas_trabajadas
            FROM registros_asistencia
            WHERE id_empleado = :id_empleado
        """

        # Si no se proporciona un rango de fechas, usar el mes actual
        if not start_date and not end_date:
            # Obtener el mes y año actual
            current_month_start = datetime.now().strftime('%Y-%m-01')
            current_month_end = datetime.now().strftime('%Y-%m-%d')

            query += " AND fecha BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND LAST_DAY(TO_DATE(:start_date, 'YYYY-MM-DD'))"
            cursor.execute(query, id_empleado=employee_id, start_date=current_month_start)
        else:
            # Si se proporciona un rango de fechas, utilizarlo
            query += " AND fecha BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD') AND TO_DATE(:end_date, 'YYYY-MM-DD')"
            cursor.execute(query, id_empleado=employee_id, start_date=start_date, end_date=end_date)

        # Obtener los resultados de la consulta
        rows = cursor.fetchall()

        # Formatear los resultados en una lista de listas para la tabla
        data = [[row[0], f"{row[1]} horas"] for row in rows]

        return data

    except cx_Oracle.DatabaseError as e:
        print(f"Error al obtener las horas trabajadas: {e}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()