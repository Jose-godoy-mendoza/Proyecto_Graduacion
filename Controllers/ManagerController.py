from Models.ManagerModel import get_employees_with_hours
from Models.ManagerModel import get_manager_email
from Models.EmployeesModel import get_work_hours
from Controllers.PdfController import generar_pdf, send_email_with_password, enviar_payslip_por_correo
from datetime import datetime, timedelta

def fetch_employees_data():
    # Llama a la función del modelo y devuelve la información
    employees_data = get_employees_with_hours()
    return employees_data

def send_report(Manager_Id, Employee_name, Employee_Id, start_date=None, end_date=None):
    
    if not start_date or not end_date:
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Definir la fecha de inicio y fin como todo el mes actual
        start_date = datetime(current_year, current_month, 1)  # Primer día del mes
        # Último día del mes actual
        if current_month == 12:
            end_date = datetime(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(current_year, current_month + 1, 1) - timedelta(days=1)


    # Obtener el correo del empleado desde la base de datos
    employee_info = get_manager_email(Manager_Id)
    if employee_info:
        email = employee_info
        print(f"Email: {email}")
    else:
        print("Empleado no encontrado")

    # Obtener las horas trabajadas del empleado
    horas_trabajadas = get_work_hours(Employee_Id, start_date, end_date)

    # Generar el reporte en PDF
    generar_pdf(Employee_name, horas_trabajadas, email)


def enviar_payslip_manager(employee_id, nombre_empleado, fecha_inicio, fecha_fin, total_horas, monto, Manager_id):
    employee_info = get_manager_email(Manager_id)
    enviar_payslip_por_correo(employee_id, nombre_empleado, employee_info, fecha_inicio, fecha_fin, total_horas, monto)