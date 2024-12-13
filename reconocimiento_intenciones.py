# Importar la clase BaseDatosIntenciones desde el archivo BD_intenciones.py
from BD_intenciones import BaseDatosIntenciones
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder

class ReconocimientoIntenciones:
    def __init__(self, db_path='intenciones.db'):
        self.db = BaseDatosIntenciones(db_path)
        self.vectorizador = TfidfVectorizer()
        self.encoder = LabelEncoder()
        self.modelo = None
        self.entrenar_modelo()

    def obtener_datos_entrenamiento(self):
        # Cargar los comandos desde la base de datos
        intenciones = self.db.obtener_intenciones()
        comandos = [intencion[1] for intencion in intenciones]
        comandos_aproximados = [intencion[2] for intencion in intenciones]
        return comandos + comandos_aproximados, [intencion[1] for intencion in intenciones] * 2

    def entrenar_modelo(self):
        # Obtener los datos de entrenamiento desde la base de datos
        frases, intenciones = self.obtener_datos_entrenamiento()

        # Codificar las intenciones
        intenciones_codificadas = self.encoder.fit_transform(intenciones)

        # Crear un pipeline con TfidfVectorizer y un clasificador SVM
        self.modelo = make_pipeline(self.vectorizador, SVC(kernel='linear'))

        # Entrenar el modelo
        self.modelo.fit(frases, intenciones_codificadas)

    def predecir_intencion(self, comando_usuario):
        # Predecir la intención de un comando
        intencion_codificada = self.modelo.predict([comando_usuario])[0]
        return self.encoder.inverse_transform([intencion_codificada])[0]
    
    def cerrar_conexion(self):
        self.db.cerrar_conexion()
