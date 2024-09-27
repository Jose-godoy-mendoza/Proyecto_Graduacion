#pyodbc.Error: ('HYC00', '[HYC00] [Microsoft][ODBC SQL Server Driver]Característica opcional no implementada (0) (SQLBindParameter)')

from Models.EmployeesModel import get_work_hours, get_employee_email
from Controllers.PdfController import generar_pdf
from datetime import datetime


def update_table_with_dates(self, employee_id, start_date, end_date):
        # Convertir fechas
        start_date_formatted = datetime.strptime(start_date, "%m/%d/%y").date()
        end_date_formatted = datetime.strptime(end_date, "%m/%d/%y").date()
        data = get_work_hours(employee_id, start_date_formatted, end_date_formatted)
        self.view.update_table(data)

def fetch_work_hours(employee_id, start_date=None, end_date=None):
    return get_work_hours(employee_id, start_date, end_date)


def send_report(employee_id, start_date=None, end_date=None):
    # Obtener el correo del empleado desde la base de datos
    email = get_employee_email(employee_id)
    
    if email is None:
        print(f"El empleado con ID {employee_id} no tiene un correo registrado.")
        return

    # Obtener las horas trabajadas del empleado
    horas_trabajadas = get_work_hours(employee_id, start_date, end_date)

    # Obtener el nombre del empleado (puedes agregar la lógica si es necesario)
    # Suponiendo que tienes una función para obtener el nombre del empleado
    employee_name = "Nombre del empleado"  # Actualiza con la función adecuada si tienes una

    # Generar el reporte en PDF
    generar_pdf(employee_name, horas_trabajadas, email)