from Models.UsersModel import UsuariosModel
import tkinter as tk
from tkinter import messagebox
from Views.EmployeeView import start_Employee_View
from Models.DatabaseModel import get_db_connection
from Models.EmployeesModel import get_employee_by_credentials
from Views.ManagerView import start_manager_view

from datetime import datetime

#from Views.ManagerView import ManagerView


def authenticate_user(username, password):
    employee = get_employee_by_credentials(username, password)
    
    if employee:
        # Si el empleado tiene rol de admin
        if employee[3] == 'administrador':  
            print(f"Bienvenido Manager {employee[1]} {employee[2]}")
            # Llama a la vista del admin
            start_manager_view(employee[0])
        else:
            print(f"Bienvenido Empleado {employee[1]} {employee[2]}")
            # Llama a la vista del Empleado
            start_Employee_View(employee[0], employee[1], employee[2])  
    else:
        print("Usuario o contraseña incorrectos")

def login(username, password):
    user = authenticate_user(username, password)
    return user


def reset_password_controller(nombre_usuario, nueva_contraseña):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Verificar si el usuario existe
    query = "SELECT e.Id_empleado FROM empleados e JOIN usuarios u ON e.Id_empleado = u.id_empleado WHERE u.nombre_usuario = ?"
    cursor.execute(query, (nombre_usuario,))
    empleado = cursor.fetchone()

    if empleado:
        id_empleado = empleado[0]

        # Actualizar la contraseña en la base de datos
        update_query = "UPDATE usuarios SET contraseña = ? WHERE id_empleado = ?"
        cursor.execute(update_query, (nueva_contraseña, id_empleado))
        connection.commit()

        cursor.close()
        connection.close()
        return True
    else:
        cursor.close()
        connection.close()
        return False