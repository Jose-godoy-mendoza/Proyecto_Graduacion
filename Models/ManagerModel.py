from Models.DatabaseModel import get_db_connection
from Controllers.PdfController import send_email_with_password
from datetime import datetime
import secrets


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





def generate_username(nombre, apellido):
    """Generar un nombre de usuario único basado en el nombre y apellido."""
    return f"{nombre.lower()}.{apellido.lower()}"

def generate_password():
    """Generar una contraseña aleatoria de 8 caracteres."""
    return secrets.token_urlsafe(8)

def insert_employee(nombre, apellido, email, fecha_ingreso, telefono):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insertar el empleado en la tabla empleados
    query_empleado = """
    INSERT INTO empleados (nombre, apellido, email, fecha_ingreso, telefono)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query_empleado, (nombre, apellido, email, fecha_ingreso, telefono))

    # Obtener el ID del nuevo empleado
    employee_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

    # Crear usuario y contraseña
    nombre_usuario = generate_username(nombre, apellido)
    contraseña = generate_password()

    # Insertar el usuario en la tabla Usuario
    query_usuario = """
    INSERT INTO Usuarios (Id_empleado, nombre_usuario, Contraseña, Rol)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(query_usuario, (employee_id, nombre_usuario, contraseña, 'empleado'))  # 'empleado' como Rol por defecto

    connection.commit()
    cursor.close()
    connection.close()

    # Enviar la contraseña por correo electrónico usando el PdfController
    send_email_with_password(email, nombre_usuario, contraseña)