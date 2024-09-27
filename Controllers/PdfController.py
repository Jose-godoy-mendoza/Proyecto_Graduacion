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

