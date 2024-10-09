from Models.DatabaseModel import get_db_connection

def modify_hours_controller(employee_id, date, new_hours):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Actualizar las horas trabajadas en la tabla 'horas_trabajadas'
    query = """
        UPDATE horas_trabajadas
        SET horas_totales = ?
        WHERE id_empleado = ? AND fecha = ?
    """
    cursor.execute(query, (new_hours, employee_id, date))

    # Verificar si se actualizó alguna fila
    if cursor.rowcount > 0:
        connection.commit()
        cursor.close()
        connection.close()
        return True
    else:
        cursor.close()
        connection.close()
        return False



def add_hours_controller(employee_id, date_str, new_hours):
    # Suponemos que el formato de fecha es correcto y las horas ya están validadas
    try:
        # Crear conexión con la base de datos
        connection = get_db_connection()

        # Crear un cursor para ejecutar la consulta
        cursor = connection.cursor()

        # Insertar las nuevas horas trabajadas en la tabla correspondiente
        query = """
        INSERT INTO horas_trabajadas (id_empleado, fecha, horas_Totales)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (employee_id, date_str, new_hours))

        # Confirmar los cambios
        connection.commit()

        # Cerrar la conexión
        cursor.close()
        connection.close()

        return True  # Devolver éxito

    except Exception as e:
        print(f"Error al agregar las horas: {e}")
        return False  # Devolver fallo
