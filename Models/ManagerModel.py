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
    WHERE MONTH(h.fecha) = MONTH(GETDATE()) 
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