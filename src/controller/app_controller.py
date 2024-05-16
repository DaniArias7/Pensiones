import psycopg2
from src.model.user import Usuario
import secret_config

class ControladorPensiones:
    def CrearTablas(self):
        """Crea las tablas necesarias en la base de datos"""
        cursor = self.ObtenerCursor()

        # Crear tabla de usuarios
        cursor.execute("""DROP TABLE IF EXISTS usuarios CASCADE""")
        cursor.execute("""CREATE TABLE usuarios (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        UNIQUE (name, age)
                        )""")

        # Crear tabla de pensiones
        cursor.execute("""DROP TABLE IF EXISTS pensiones""")
        cursor.execute("""CREATE TABLE pensiones (
                        id SERIAL PRIMARY KEY,
                        usuario_id INTEGER NOT NULL,
                        ahorro_pensional FLOAT NOT NULL,
                        pension FLOAT NOT NULL,
                        UNIQUE (usuario_id, ahorro_pensional, pension),
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                        )""")

        cursor.connection.commit()

    def InsertarUsuario(self, usuario):
        """Inserta un nuevo usuario en la base de datos"""
        cursor = self.ObtenerCursor()
        try:
            cursor.execute("""INSERT INTO usuarios (name, age)
                          VALUES (%s, %s) RETURNING id""",
                        (usuario.name, usuario.age))
            usuario_id = cursor.fetchone()[0]
            usuario.id = usuario_id
            cursor.connection.commit()
        except psycopg2.IntegrityError as e:
            cursor.connection.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Error: Ya existe un usuario con el nombre '{usuario.name}' y la edad {usuario.age}.")
            else:
                print(f"Error: {e}")

    def InsertarPension(self, usuario_id, ahorro_pensional, pension):
        """Inserta una nueva pensión en la base de datos"""
        cursor = self.ObtenerCursor()
        try:
            cursor.execute("""INSERT INTO pensiones (usuario_id, ahorro_pensional, pension)
                          VALUES (%s, %s, %s)""",
                        (usuario_id, ahorro_pensional, pension))
            cursor.connection.commit()
        except psycopg2.IntegrityError as e:
            cursor.connection.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                print("Error: Ya existe una pensión con los mismos datos para este usuario.")
            else:
                print(f"Error: {e}")

    def ModificarUsuario(self, usuario):
        """Modifica los datos de un usuario existente"""
        cursor = self.ObtenerCursor()
        cursor.execute("""UPDATE usuarios
                          SET name = %s, age = %s
                          WHERE id = %s""",
                       (usuario.name, usuario.age, usuario.id))
        cursor.connection.commit()

    def EliminarUsuario(self, usuario_id):
        """Elimina un usuario y sus pensiones asociadas"""
        cursor = self.ObtenerCursor()
        cursor.execute("""DELETE FROM pensiones WHERE usuario_id = %s""", (usuario_id,))
        cursor.execute("""DELETE FROM usuarios WHERE id = %s""", (usuario_id,))
        cursor.connection.commit()

    def ObtenerUsuarios(self):
        """Obtiene todos los usuarios de la base de datos"""
        cursor = self.ObtenerCursor()
        cursor.execute("""SELECT id, name, age
                          FROM usuarios""")
        usuarios = []
        for fila in cursor.fetchall():
            usuario = Usuario(fila[1], fila[2], "soltero")
            usuario.id = fila[0]
            usuarios.append(usuario)
        return usuarios

    def ObtenerPensiones(self, usuario_id):
        """Obtiene todas las pensiones de un usuario"""
        cursor = self.ObtenerCursor()
        cursor.execute("""SELECT id, ahorro_pensional, pension
                          FROM pensiones
                          WHERE usuario_id = %s""", (usuario_id,))
        pensiones = []
        for fila in cursor.fetchall():
            pension = {"id": fila[0], "ahorro_pensional": fila[1], "pension": fila[2]}
            pensiones.append(pension)
        return pensiones

    def ObtenerCursor(self):
        """Crea la conexión a la base de datos y retorna un cursor para hacer consultas"""
        connection = psycopg2.connect(database=secret_config.PGDATABASE, user=secret_config.PGUSER,
                                      password=secret_config.PGPASSWORD, host=secret_config.PGHOST)
        cursor = connection.cursor()
        return cursor