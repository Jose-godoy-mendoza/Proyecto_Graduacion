from Models.UsersModel import UsuariosModel
import tkinter as tk
from tkinter import messagebox
from Views.EmployeeView import start_Employee_View
from Models.DatabaseModel import get_db_connection
from Models.EmployeesModel import get_employee_by_credentials, get_work_hours

from datetime import datetime

#from Views.ManagerView import ManagerView


def authenticate_user(username, password):
    employee = get_employee_by_credentials(username, password)
    
    if employee:
        print(f"Bienvenido {employee[0]} {employee[1]} {employee[2]}")
        #login_window.destroy()  # Cierra la ventana de login correctamente
        start_Employee_View(employee[0], employee[1], employee[2])  # Redirige a la vista de empleados
    else:
        print("Usuario o contraseña incorrectos")
        # No cerramos la ventana, solo mostramos el error en la vista de login

def login(username, password):
    user = authenticate_user(username, password)
    return user

