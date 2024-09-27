#pyodbc.Error: ('HYC00', '[HYC00] [Microsoft][ODBC SQL Server Driver]Característica opcional no implementada (0) (SQLBindParameter)')

from Models.EmployeesModel import get_work_hours
from datetime import datetime


def update_table_with_dates(self, employee_id, start_date, end_date):
        # Convertir fechas
        start_date_formatted = datetime.strptime(start_date, "%m/%d/%y").date()
        end_date_formatted = datetime.strptime(end_date, "%m/%d/%y").date()
        data = get_work_hours(employee_id, start_date_formatted, end_date_formatted)
        self.view.update_table(data)

def fetch_work_hours(employee_id, start_date=None, end_date=None):
    return get_work_hours(employee_id, start_date, end_date)