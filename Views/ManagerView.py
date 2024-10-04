import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from Controllers.ManagerController import get_employees_with_hours, send_report
from Models.EmployeesModel import get_work_hours





# Función para mostrar la ventana con el reporte específico de un empleado
def mostrar_reporte_empleado(Employee_id, nombre_empleado, Manager_Id):
    ventana_empleado = tk.Toplevel(root)
    ventana_empleado.title(f"Reporte de {Employee_id, nombre_empleado}")

    # Título de la ventana
    ttk.Label(ventana_empleado, text=f"Reporte de Horas Trabajadas - {nombre_empleado}", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Tabla para las horas trabajadas del empleado seleccionado
    columns = ("Día", "Horas trabajadas")
    Employee_Table = ttk.Treeview(ventana_empleado, columns=columns, show="headings")
    Employee_Table.heading("Día", text="Día")
    Employee_Table.heading("Horas trabajadas", text="Horas trabajadas")
    Employee_Table.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    
    data = get_work_hours(Employee_id)

    update_table(Employee_Table, data)

    # Selección de rango de fechas
    ttk.Label(ventana_empleado, text="Seleccionar rango de fechas:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    ttk.Label(ventana_empleado, text="Desde:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    start_date_entry = DateEntry(ventana_empleado)
    start_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

    ttk.Label(ventana_empleado, text="Hasta:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    end_date_entry = DateEntry(ventana_empleado)
    end_date_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)

    # Botón para actualizar el reporte por rango de fechas
    def update_table_with_dates():
        # Obtener las fechas seleccionadas
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()
        
        # Llamar a la función del modelo para obtener las horas trabajadas
        data = get_work_hours(Employee_id, start_date, end_date)
        
        # Actualizar la tabla con los nuevos datos
        update_table(Employee_Table, data)

    update_button = ttk.Button(ventana_empleado, text="Actualizar reporte", command=update_table_with_dates)
    update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def Send_PDF():
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()
        send_report(Manager_Id, nombre_empleado, Employee_id, start_date, end_date)

    send_button = ttk.Button(ventana_empleado, text="Enviar reporte por correo", command=Send_PDF)
    send_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

def update_table(Employee_Table, data):
    # Limpiar la tabla
    for row in Employee_Table.get_children():
        Employee_Table.delete(row)

    # Insertar los nuevos datos
    for row_data in data:
        Employee_Table.insert("", tk.END, values=row_data)

def start_manager_view(Manager_Id):
    global root
    # Crear la ventana principal para el gerente
    root = tk.Tk()
    root.title("Panel del Gerente - Reporte de Horas Trabajadas")
    # Menú superior
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Menú para opciones como cerrar sesión o ver perfil
    opciones_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opciones", menu=opciones_menu)
    opciones_menu.add_command(label="Cerrar sesión", command=root.quit)

    # Título para la tabla
    ttk.Label(root, text="Reporte de Horas Trabajadas - Todos los Empleados", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # Tabla para mostrar las horas trabajadas por todos los empleados
    columns = ("ID","Empleado",  "Horas trabajadas", "Ver más")
    table = ttk.Treeview(root, columns=columns, show="headings")
    table.heading("ID", text="ID")
    table.heading("Empleado", text="Empleado")
    table.heading("Horas trabajadas", text="Horas trabajadas")
    table.heading("Ver más", text="Ver más")
    table.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    

    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER)

    # Obtener los datos de empleados y horas trabajadas
    employees_data = get_employees_with_hours()

    # Insertar los datos en la tabla
    for employee in employees_data:
        # Combinar nombre y apellido en el primer valor
        nombre_completo = f"{employee[1]}"  # Asegúrate de que esto sea correcto según tu consulta
        table.insert("", tk.END, values=(employee[0],nombre_completo, employee[2], "Ver más"))  # El último valor es un texto para el botón

    # Función para manejar el clic en "Ver más"
    def on_treeview_click(event):
        item = table.selection()[0]
        id_empleado = table.item(item, "values")[0]
        nombre_empleado = table.item(item, "values")[1]
        mostrar_reporte_empleado(id_empleado, nombre_empleado, Manager_Id)

    # Asociar el clic en la tabla con la función "Ver más"
    table.bind("<Double-1>", on_treeview_click)

    root.mainloop()
