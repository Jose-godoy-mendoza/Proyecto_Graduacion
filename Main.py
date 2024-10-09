import tkinter as tk
from tkinter import ttk
from tkinter import Label, messagebox
import cv2
from PIL import Image, ImageTk
from Controllers.LoginController import login
from Models.EmployeesModel import get_employee_profile, update_employee_profile, get_work_hours
from Models.ManagerModel import get_employees_with_hours
from Controllers.LoginController import reset_password_controller



def open_reset_password_window():
    # Crear ventana emergente
    reset_window = tk.Toplevel(root)
    reset_window.title("Recuperar Contraseña")
    reset_window.geometry("300x350")

    # Etiqueta y campo para ingresar el nombre de usuario
    username_label = tk.Label(reset_window, text="Usuario")
    username_label.pack(pady=5)
    username_entry = ttk.Entry(reset_window)
    username_entry.pack(pady=5)

    # Etiqueta y campo para ingresar la nueva contraseña
    new_password_label = tk.Label(reset_window, text="Nueva Contraseña")
    new_password_label.pack(pady=5)
    new_password_entry = ttk.Entry(reset_window, show="*")
    new_password_entry.pack(pady=5)

    # Etiqueta y campo para confirmar la nueva contraseña
    confirm_password_label = tk.Label(reset_window, text="Confirmar Contraseña")
    confirm_password_label.pack(pady=5)
    confirm_password_entry = ttk.Entry(reset_window, show="*")
    confirm_password_entry.pack(pady=5)

    # Botón para enviar la solicitud de restablecimiento
    submit_button = ttk.Button(reset_window, text="Restablecer Contraseña", command=lambda: reset_password(username_entry.get(), new_password_entry.get(), confirm_password_entry.get(), reset_window))
    submit_button.pack(pady=10)


def reset_password(username, new_password, confirm_password, window):
    if not username:
        messagebox.showerror("Error", "El nombre de usuario es obligatorio.")
        return

    if not new_password or not confirm_password:
        messagebox.showerror("Error", "Debe ingresar y confirmar la nueva contraseña.")
        return

    if new_password != confirm_password:
        messagebox.showerror("Error", "Las contraseñas no coinciden.")
        return

    success = reset_password_controller(username, new_password)
    if success:
        messagebox.showinfo("Éxito", "Su contraseña ha sido actualizada exitosamente.")
        window.destroy()  # Cerrar la ventana de restablecimiento
    else:
        messagebox.showerror("Error", "No se pudo restablecer la contraseña. Verifique su nombre de usuario.")




# Función para actualizar la imagen de la cámara en la interfaz
def update_frame():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.config(image=imgtk)
    camera_label.after(10, update_frame)


#get_work_hours(1)

# Inicializar ventana principal
root = tk.Tk()
root.title("Reconocimiento Facial - Aplicación")
root.geometry("1000x600")

# Usar ttk y estilos modernos
style = ttk.Style()
style.theme_use('clam')  
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12))

# Fondo de la ventana
background_frame = tk.Frame(root, bg="#2C3E50")
background_frame.place(relwidth=1, relheight=1)

# Título
title_label = tk.Label(background_frame, text="Sistema de Reconocimiento Facial", 
                       font=('Helvetica', 24), fg="white", bg="#2C3E50")
title_label.place(x=250, y=20)

# Crear la parte izquierda para mostrar la cámara
camera_frame = tk.Frame(background_frame, bg="white")
camera_frame.place(x=50, y=100, width=640, height=480)

camera_label = Label(camera_frame)
camera_label.pack(fill=tk.BOTH, expand=True)

# Simulación del nombre reconocido
name_label = tk.Label(background_frame, text="Nombre:", font=('Helvetica', 18), fg="white", bg="#2C3E50")
name_label.place(x=750, y=100)

# Etiqueta para mostrar el nombre reconocido
name_label = tk.Label(background_frame, text="Desconocido", font=("Helvetica", 18), fg="green", bg="#2C3E50")
name_label.place(x=750, y=140)

# Simulación del formulario de inicio de sesión
login_frame = tk.Frame(background_frame, bg="#34495E")
login_frame.place(x=750, y=200, width=220, height=320)

login_label = tk.Label(login_frame, text="Iniciar Sesión", font=('Helvetica', 16), fg="white", bg="#34495E")
login_label.pack(pady=10)

username_label = tk.Label(login_frame, text="Usuario", font=('Helvetica', 12), fg="white", bg="#34495E")
username_label.pack(pady=5)
username_entry = ttk.Entry(login_frame)
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Contraseña", font=('Helvetica', 12), fg="white", bg="#34495E")
password_label.pack(pady=5)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack(pady=5)


def on_login_click():
        username = username_entry.get()
        password = password_entry.get()
        result = login(username, password)  # Llamamos al controlador y pasamos los datos
        if result:  # Si el login fue exitoso
            messagebox.showinfo("Login exitoso", f"Bienvenido, {result[1]} {result[2]}")
            #root.destroy()  # Cerrar ventana de login
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")


login_button = ttk.Button(login_frame, text="Entrar", command=on_login_click)
login_button.pack(pady=20)

# Botón de "Recuperar contraseña"
reset_password_button = ttk.Button(login_frame, text="Recuperar contraseña", command=open_reset_password_window)
reset_password_button.pack(pady=10)


# Iniciar la cámara
cap = cv2.VideoCapture(0)
update_frame()

# Iniciar la ventana principal
root.mainloop()

# Liberar la cámara cuando se cierra la ventana
cap.release()
cv2.destroyAllWindows()
