# BD_intenciones.py
import sqlite3
from cryptography.fernet import Fernet # type: ignore

class BaseDatosIntenciones:
    def __init__(self, db_path='intenciones.db'):
        # Usar una clave fija en lugar de generar una nueva cada vez
        # La clave debe ser una cadena de 32 bytes de base64
        self.clave = b'gG-kiGv2kXfbmZQFwR4u-l1g6lG5W8Xp2s_EvXjU5Kk='  # Ejemplo de clave válida generada
        self.cifrador = Fernet(self.clave)
        self.conexion = sqlite3.connect(db_path)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS intenciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comando BLOB NOT NULL,
                comando_aproximado BLOB NOT NULL
            )
        """)
        self.conexion.commit()

    def insertar_intencion(self, comando, comando_aproximado):
        # Cifrar los comandos antes de insertarlos
        comando_cifrado = self.cifrador.encrypt(comando.encode())
        comando_aprox_cifrado = self.cifrador.encrypt(comando_aproximado.encode())
        self.cursor.execute(
            "INSERT INTO intenciones (comando, comando_aproximado) VALUES (?, ?)",
            (comando_cifrado, comando_aprox_cifrado)
        )
        self.conexion.commit()

    def obtener_intenciones(self):
        self.cursor.execute("SELECT id, comando, comando_aproximado FROM intenciones")
        registros = self.cursor.fetchall()
        # Desencriptar los comandos al leerlos
        return [
            (
                registro[0],
                self.cifrador.decrypt(registro[1]).decode(),
                self.cifrador.decrypt(registro[2]).decode()
            )
            for registro in registros
        ]

    def cerrar_conexion(self):
        try:
            self.conexion.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

