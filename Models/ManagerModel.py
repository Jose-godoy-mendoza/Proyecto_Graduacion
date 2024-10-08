from Models.DatabaseModel import get_db_connection
from datetime import datetime

def get_employees_with_hours():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT e.Id_empleado, 
           CONCAT(e.nombre, ' ', e.apellido) AS nombre_completo, 
           COALESCE(SUM(h.horas_totales), 0) AS total_horas
    FROM empleados e
    LEFT JOIN horas_trabajadas h ON e.Id_empleado = h.id_empleado 
       AND MONTH(h.fecha) = MONTH(GETDATE()) 
       AND YEAR(h.fecha) = YEAR(GETDATE())
    GROUP BY e.Id_empleado, e.nombre, e.apellido
    """

    cursor.execute(query)
    results = cursor.fetchall()
    print(results)
    cursor.close()
    connection.close()

    return results

def get_manager_email(Manager_Id):
    # Conectar a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Definir la consulta para obtener el correo electrónico
    query = "SELECT email FROM empleados WHERE id_empleado = ?"
    cursor.execute(query, (Manager_Id,))

    # Obtener el resultado
    result = cursor.fetchone()

    # Cerrar la conexión
    cursor.close()
    connection.close()

    if result:
      return result[0]
    else:
        return None  # Si no se encuentra, retorna None
    
def Delete_Employee(employee_id):
    try:
        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        # Consulta SQL para eliminar al empleado
        query = "DELETE FROM empleados WHERE Id_empleado = ?;"
        
        # Ejecutar la consulta
        cursor.execute(query, (employee_id,))
        
        # Confirmar los cambios
        connection.commit()

        print(f"Empleado con ID {employee_id} eliminado correctamente.")

    except Exception as e:
        print(f"Error al eliminar el empleado: {e}")

    finally:
        # Cerrar la conexión
        if connection:
            connection.close()


def insert_employee(nombre, apellido, email, fecha_ingreso, telefono):
    connection = get_db_connection()
    cursor = connection.cursor()
    # Aquí iría la inserción del nuevo empleado en la base de datos
    query = """INSERT INTO Empleados (Nombre, Apellido, Email, fecha_ingreso, telefono)
               VALUES (?, ?, ?, ?, ?)"""  # Usa '?' como marcadores
    cursor.execute(query, (nombre, apellido, email, fecha_ingreso, telefono))
    connection.commit()
    print("Empleado creado correctamente")