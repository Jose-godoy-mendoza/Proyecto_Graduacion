from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText


def generar_pdf(nombre_empleado, horas_trabajadas, email_empleado):
    # Crear un archivo PDF
    archivo_pdf = "reporte_horas_trabajadas.pdf"
    pdf = SimpleDocTemplate(archivo_pdf, pagesize=letter)

    # Contenido para agregar al PDF
    elementos = []

    # Agregar el título
    estilos = getSampleStyleSheet()
    titulo = Paragraph(f"<b>Reporte de Horas Trabajadas para {nombre_empleado}</b>", estilos['Title'])
    elementos.append(titulo)

    # Datos de la tabla, incluyendo la fila de encabezado
    datos_tabla = [["Fecha", "Horas Totales"]]
    for fecha, horas in horas_trabajadas:
        datos_tabla.append([fecha, horas])

    # Crear la tabla con estilos
    tabla = Table(datos_tabla, colWidths=[2 * inch, 2 * inch])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Agregar la tabla a los elementos
    elementos.append(tabla)

    # Construir el PDF
    pdf.build(elementos)

    # Enviar el informe por correo
    enviar_email(archivo_pdf, email_empleado)

    # Eliminar el archivo PDF después de enviarlo
    os.remove(archivo_pdf)

def enviar_email(archivo_pdf, email_destino):
    email_remitente = "jgodoymnedoza@gmail.com"  # Tu correo de Gmail
    password = "eouh buim wcuj jksl"  # Usa aquí la contraseña de aplicación generada

    # Crear el correo electrónico
    mensaje = MIMEMultipart()
    mensaje['From'] = email_remitente
    mensaje['To'] = email_destino
    mensaje['Subject'] = "Reporte de Horas Trabajadas"

    # Adjuntar el archivo PDF
    adjunto = open(archivo_pdf, "rb")
    parte = MIMEBase('application', 'octet-stream')
    parte.set_payload(adjunto.read())
    encoders.encode_base64(parte)
    parte.add_header('Content-Disposition', f'attachment; filename={archivo_pdf}')
    mensaje.attach(parte)
    adjunto.close()

    # Enviar el correo
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()  # Iniciar la conexión segura
            servidor.login(email_remitente, password)  # Autenticar en Gmail
            servidor.send_message(mensaje)  # Enviar el mensaje
            print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

#eouh buim wcuj jksl

def send_email_with_password(to_email, nombre_usuario, contraseña):
    """Función para enviar el nombre de usuario y la contraseña al empleado por correo electrónico."""
    email_remitente = "jgodoymnedoza@gmail.com"  # Tu correo de Gmail
    password = "eouh buim wcuj jksl"  # Usa aquí la contraseña de aplicación generada

    subject = "Detalles de tu cuenta de acceso"
    message = f"""
    Hola,

    Tu cuenta ha sido creada exitosamente.

    Usuario: {nombre_usuario}
    Contraseña: {contraseña}

    
    Saludos,
    El equipo de soporte
    """

    # Configurar el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = email_remitente
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Enviar el correo usando smtplib
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Cambia por el servidor SMTP que uses (Gmail, Outlook, etc.)
        server.starttls()
        server.login(email_remitente, password)
        text = msg.as_string()
        server.sendmail(email_remitente, to_email, text)
        server.quit()
        print(f"Contraseña enviada correctamente a {to_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


def enviar_payslip_por_correo(employee_id, nombre_empleado, manager_email, fecha_inicio, fecha_fin, total_horas, monto):

    # Detalles del correo
    email_remitente = "jgodoymnedoza@gmail.com"  # Tu correo de Gmail
    password = "eouh buim wcuj jksl"  # Usa aquí la contraseña de aplicación generada

    # Crear el mensaje del correo
    mensaje = MIMEMultipart()
    mensaje['From'] = email_remitente
    mensaje['To'] = manager_email
    mensaje['Subject'] = f"Payslip del Empleado {employee_id} - {nombre_empleado}"

    # Contenido del correo
    body = f"""
    Estimado Supervisor,

    A continuación, se detalla la payslip del empleado {nombre_empleado}:

    Fecha Inicio: {fecha_inicio}
    Fecha Fin: {fecha_fin}
    Total de horas trabajadas: {total_horas}
    Total a pagar: {monto}

    Atentamente,
    Sistema de Gestión de Empleados
    """
    
    mensaje.attach(MIMEText(body, 'plain'))

    try:
        # Conectar al servidor SMTP de tu proveedor de correo (por ejemplo, Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Cambia esto según tu proveedor de correo
        server.starttls()
        server.login(email_remitente, password)

        # Enviar el correo
        server.send_message(mensaje)
        server.quit()
        print(f"Correo enviado a {manager_email}")
    except Exception as e:
        print(f"No se pudo enviar el correo: {e}")