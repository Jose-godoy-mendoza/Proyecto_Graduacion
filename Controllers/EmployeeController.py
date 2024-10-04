#pyodbc.Error: ('HYC00', '[HYC00] [Microsoft][ODBC SQL Server Driver]Característica opcional no implementada (0) (SQLBindParameter)')

from Models.EmployeesModel import get_work_hours, get_employee_email_name
from Controllers.PdfController import generar_pdf
from datetime import datetime, timedelta


def update_table_with_dates(self, employee_id, start_date, end_date):
        # Convertir fechas
        start_date_formatted = datetime.strptime(start_date, "%m/%d/%y").date()
        end_date_formatted = datetime.strptime(end_date, "%m/%d/%y").date()
        data = get_work_hours(employee_id, start_date_formatted, end_date_formatted)
        self.view.update_table(data)

def fetch_work_hours(employee_id, start_date=None, end_date=None):
    return get_work_hours(employee_id, start_date, end_date)


def send_report(employee_id, start_date=None, end_date=None):
    
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
    employee_info = get_employee_email_name(employee_id)
    if employee_info:
        email = employee_info['email']
        nombre = employee_info['nombre']
        apellido = employee_info['apellido']
        # Puedes usar los valores como necesites
        print(f"Email: {email}, Nombre: {nombre}, Apellido: {apellido}")
    else:
        print("Empleado no encontrado")

    # Obtener las horas trabajadas del empleado
    horas_trabajadas = get_work_hours(employee_id, start_date, end_date)

    # Obtener el nombre del empleado (puedes agregar la lógica si es necesario)
    # Suponiendo que tienes una función para obtener el nombre del empleado
    employee_name = nombre + " " + apellido  # Actualiza con la función adecuada si tienes una

    # Generar el reporte en PDF
    generar_pdf(employee_name, horas_trabajadas, email)