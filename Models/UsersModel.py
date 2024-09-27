from Models.DatabaseModel import get_db_connection

class UsuariosModel:
    def __init__(self):
        # Establecer la conexión a la base de datos
        self.Conection = get_db_connection
        self.cursor = self.Conection.cursor()

    def obtener_usuario(self, UserName, Password):
        # Consultar en la tabla de usuarios
        query = "SELECT * FROM Usuario WHERE nombre_usuario = ? AND Contraseña = ?"
        self.cursor.execute(query, (UserName, Password))
        usuario = self.cursor.fetchone()
        
        if usuario:
            # Retornar un diccionario con los datos del usuario
            return {
                'Id_usuario': usuario[0],
                'Id_empleado': usuario[1],
                'nombre_usuario': usuario[2],
                'Rol': usuario[4]  # Asumiendo que el campo Rol está en la posición 4
            }
        else:
            return None
