import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from Models.EmployeesModel import get_employee_profile, update_employee_profile, get_work_hours
from Controllers.EmployeeController import fetch_work_hours


def Pull_Up_Profile(Employee_id, Nombre):
    perfil_window = tk.Toplevel(root)
    perfil_window.title("Perfil del Empleado")

    # Información de ejemplo del empleado (puedes cambiarlo cuando integres la base de datos)
    email, telefono = get_employee_profile(Employee_id)

    if email and telefono:
        Name = Nombre
        Email = email
        Phone = telefono
    else:
        Name = "No se encontró información"
        Email = "Desconocido"
        Phone = "Desconocido"

    # Etiquetas y campos para editar la información de contacto
    ttk.Label(perfil_window, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
    ttk.Label(perfil_window, text=Name).grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

    ttk.Label(perfil_window, text="Correo electrónico:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
    email_entry = ttk.Entry(perfil_window)
    email_entry.insert(0, Email)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(perfil_window, text="Número de teléfono:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
    telefono_entry = ttk.Entry(perfil_window)
    telefono_entry.insert(0, Phone)
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    # Botón para guardar los cambios (solo muestra mensaje por ahora)
    def Save_Changes():
        nuevo_email = email_entry.get()
        nuevo_telefono = telefono_entry.get()

        # Mostrar un mensaje de confirmación
        if update_employee_profile(Employee_id, nuevo_email, nuevo_telefono):
            messagebox.showinfo("Éxito", "Información actualizada correctamente.")
        else:
            messagebox.showerror("Error", "No se pudo actualizar la información.")
        perfil_window.destroy()

    ttk.Button(perfil_window, text="Guardar cambios", command=Save_Changes).grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def update_table_with_dates():
    # Obtener las fechas seleccionadas
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    
    # Llamar a la función del modelo para obtener las horas trabajadas
    data = get_work_hours(employee_id, start_date, end_date)
    
    # Actualizar la tabla con los nuevos datos
    update_table(data)


# Funciones
def update_table(data):
    # Limpiar la tabla
    for row in table.get_children():
        table.delete(row)

    # Insertar los nuevos datos
    for row_data in data:
        table.insert("", tk.END, values=row_data)

def generate_report(start_date, end_date):
    # Obtener horas trabajadas dentro del periodo seleccionado
    work_data = get_work_hours(start_date, end_date)
    file_name = "hours_report.pdf"
    
    c = canvas.Canvas(file_name, pagesize=letter)
    c.drawString(100, 750, f"Reporte de Horas Trabajadas")
    c.drawString(100, 730, f"Rango: {start_date} - {end_date}")
    
    y = 710
    for day, hours in work_data:
        c.drawString(100, y, f"{day}: {hours}")
        y -= 20  # Espaciado entre líneas
    
    c.save()
    
    return file_name

def send_email(file_name, recipient_email):
    sender_email = "tu_correo@example.com"  
    password = "tu_contraseña"  

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Reporte de Horas Trabajadas"

    part = MIMEBase('application', 'octet-stream')
    with open(file_name, 'rb') as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={file_name}')
    msg.attach(part)

    with smtplib.SMTP('smtp.example.com', 587) as server:  # Reemplaza con tu servidor SMTP
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

def generate_custom_report():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()

    if start_date > end_date:
        messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin.")
        return

    file_name = generate_report(start_date, end_date)
    messagebox.showinfo("Éxito", f"Reporte generado: {file_name}")

def send_report():
    recipient_email = "empleado@example.com"  # Aquí deberías obtener el correo del empleado desde la base de datos
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    file_name = generate_report(start_date, end_date)
    
    send_email(file_name, recipient_email)
    messagebox.showinfo("Éxito", "Reporte enviado exitosamente.")

def update_table_with_dates():
    start_date = start_date_entry.get_date()
    end_date = end_date_entry.get_date()
    if start_date > end_date:
        messagebox.showerror("Error", "La fecha de inicio no puede ser posterior a la fecha de fin.")
        return
    data = fetch_work_hours(start_date, end_date)
    update_table(data)

def log_out():
    messagebox.showinfo("Cerrar sesión", "Has cerrado sesión.")
    root.quit()


def start_Employee_View(Employee_id, Nombre, Apellido):
    # Interfaz Gráfica
    global root, table, start_date_entry, end_date_entry
    root = tk.Tk()
    root.title("Consulta de Horas Trabajadas")

    # Menú superior
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Menú archivo
    employee_name = Nombre+" "+ Apellido

    menu_bar.add_checkbutton(label="Cerrar Sesion", command=log_out)
    menu_bar.add_checkbutton(label="Perfil", command=lambda:Pull_Up_Profile(Employee_id, employee_name))

    # Simular el nombre del empleado
    
    employee_label = ttk.Label(root, text=f"Empleado: {employee_name}", font=("Helvetica", 12))
    employee_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

    # Tabla para mostrar las horas trabajadas
    columns = ("Día", "Horas trabajadas")
    table = ttk.Treeview(root, columns=columns, show="headings")
    table.heading("Día", text="Día")
    table.heading("Horas trabajadas", text="Horas trabajadas")
    table.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Inicializar tabla con datos del mes actual
    data = get_work_hours(Employee_id)  # Obtener horas trabajadas del mes actual
    update_table(data)

    # Selección de rango de fechas
    range_label = ttk.Label(root, text="Selecciona un rango de fechas:")
    range_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

    start_date_label = ttk.Label(root, text="Desde:")
    start_date_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
    start_date_entry = DateEntry(root)
    start_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.E)

    end_date_label = ttk.Label(root, text="Hasta:")
    end_date_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
    end_date_entry = DateEntry(root)
    end_date_entry.grid(row=4, column=1, padx=10, pady=5, sticky=tk.E)

    def update_table_with_dates():
        # Obtener las fechas seleccionadas
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()
        
        # Llamar a la función del modelo para obtener las horas trabajadas
        data = get_work_hours(Employee_id, start_date, end_date)
        
        # Actualizar la tabla con los nuevos datos
        update_table(data)

    # Botón para actualizar la tabla
    update_button = ttk.Button(root, text="Actualizar tabla", command=update_table_with_dates)
    update_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

    # Botón para enviar el reporte por correo
    send_button = ttk.Button(root, text="Enviar Reporte por Correo", command=send_report)
    send_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

    def on_closing():
        print("Cerrando la ventana de empleados.")
        root.destroy()  # Cierra la ventana correctamente sin errores
        exit()  # Termina el programa sin errores
    
    # Asignar la función de cierre a la ventana
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
