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

