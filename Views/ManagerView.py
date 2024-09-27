import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# Crear la ventana principal para el gerente
root = tk.Tk()
root.title("Panel del Gerente - Reporte de Horas Trabajadas")

# Función para mostrar la ventana con el reporte específico de un empleado
def mostrar_reporte_empleado(empleado):
    ventana_empleado = tk.Toplevel(root)
    ventana_empleado.title(f"Reporte de {empleado}")

    # Título de la ventana
    ttk.Label(ventana_empleado, text=f"Reporte de Horas Trabajadas - {empleado}", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Tabla para las horas trabajadas del empleado seleccionado
    columns = ("Día", "Horas trabajadas")
    table_empleado = ttk.Treeview(ventana_empleado, columns=columns, show="headings")
    table_empleado.heading("Día", text="Día")
    table_empleado.heading("Horas trabajadas", text="Horas trabajadas")
    table_empleado.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Datos de ejemplo específicos del empleado
    employee_data = [
        ("2024-09-01", "8"),
        ("2024-09-02", "8"),
        ("2024-09-03", "7.5"),
        ("2024-09-04", "8")
    ]
    
    # Insertar los datos en la tabla del empleado
    for row in employee_data:
        table_empleado.insert("", tk.END, values=row)

    # Selección de rango de fechas
    ttk.Label(ventana_empleado, text="Seleccionar rango de fechas:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    ttk.Label(ventana_empleado, text="Desde:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    start_date_entry = DateEntry(ventana_empleado)
    start_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

    ttk.Label(ventana_empleado, text="Hasta:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    end_date_entry = DateEntry(ventana_empleado)
    end_date_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)

    # Botón para actualizar el reporte por rango de fechas
    def actualizar_reporte_empleado():
        # Aquí puedes agregar la lógica para actualizar los datos del empleado según el rango de fechas seleccionado
        messagebox.showinfo("Actualizar", f"Reporte de {empleado} actualizado (simulado).")

    update_button = ttk.Button(ventana_empleado, text="Actualizar reporte", command=actualizar_reporte_empleado)
    update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Botón para enviar el reporte por correo (simulado por ahora)
    def enviar_reporte_por_correo():
        messagebox.showinfo("Enviado", f"Reporte de {empleado} enviado por correo (simulado).")

    send_button = ttk.Button(ventana_empleado, text="Enviar reporte por correo", command=enviar_reporte_por_correo)
    send_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

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
columns = ("Empleado", "Día", "Horas trabajadas", "Ver más")
table = ttk.Treeview(root, columns=columns, show="headings")
table.heading("Empleado", text="Empleado")
table.heading("Día", text="Día")
table.heading("Horas trabajadas", text="Horas trabajadas")
table.heading("Ver más", text="Ver más")
table.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

# Datos de ejemplo para la tabla general
example_data = [
    ("Juan Pérez", "2024-09-01", "8"),
    ("María López", "2024-09-01", "7"),
    ("Carlos García", "2024-09-01", "9"),
    ("Juan Pérez", "2024-09-02", "8"),
    ("María López", "2024-09-02", "7.5"),
    ("Carlos García", "2024-09-02", "8"),
]

# Insertar los datos en la tabla general
for row in example_data:
    empleado = row[0]
    table.insert("", tk.END, values=(row[0], row[1], row[2], "Ver más"))

# Función para manejar el clic en "Ver más"
def on_treeview_click(event):
    item = table.selection()[0]
    empleado = table.item(item, "values")[0]
    mostrar_reporte_empleado(empleado)

# Asociar el clic en la tabla con la función "Ver más"
table.bind("<Double-1>", on_treeview_click)

root.mainloop()
