import os
import tkinter as tk
from tkinter import filedialog
import webbrowser
import pyttsx3
import time
import threading
import keyboard

class LecturaPDF:
    listado_activo = False
    ultimo_archivo_listado = None

    @staticmethod
    def abrir_pdf_desde_descargas():
        threading.Thread(target=LecturaPDF._abrir_pdf_ventana_descargas).start()

    @staticmethod
    def _abrir_pdf_ventana_descargas():
        try:
            descargas_path = os.path.expanduser("~/Downloads")
            root = tk.Tk()
            root.withdraw()

            archivo_pdf = filedialog.askopenfilename(
                initialdir=descargas_path,
                filetypes=[("Archivos PDF", "*.pdf")],
                title="Selecciona un archivo PDF desde Descargas"
            )

            if archivo_pdf:
                webbrowser.open(archivo_pdf)
                print(f"Documento PDF abierto: {archivo_pdf}")

        except Exception as e:
            print(f"Error al abrir el archivo PDF: {e}")

    @staticmethod
    def listar_archivos():
        threading.Thread(target=LecturaPDF._listar_archivos_en_hilo).start()

    @staticmethod
    def _listar_archivos_en_hilo():
        try:
            path = os.path.expanduser("~/Downloads")
            archivos = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
            archivos.sort(key=lambda f: os.path.getmtime(os.path.join(path, f)), reverse=True)

            LecturaPDF.listado_activo = True
            engine = pyttsx3.init()
            for archivo in archivos:
                if not LecturaPDF.listado_activo:
                    break
                LecturaPDF.ultimo_archivo_listado = archivo
                engine.say(archivo)
                engine.runAndWait()
                time.sleep(1)
            print("Listado de archivos finalizado.")
        except Exception as e:
            print(f"Error al listar archivos: {e}")

    @staticmethod
    def detener_listado():
        LecturaPDF.listado_activo = False
        print("Listado de archivos detenido.")
        if LecturaPDF.ultimo_archivo_listado:
            print(f"Último archivo listado guardado: {LecturaPDF.ultimo_archivo_listado}")

    @staticmethod
    def abrir_ultimo_archivo_listado():
        if LecturaPDF.ultimo_archivo_listado:
            try:
                path = os.path.expanduser("~/Downloads")
                archivo_path = os.path.join(path, LecturaPDF.ultimo_archivo_listado)
                if os.path.exists(archivo_path):
                    os.startfile(archivo_path)
                    print(f"Archivo '{LecturaPDF.ultimo_archivo_listado}' abierto.")
                else:
                    print("El último archivo listado ya no existe en la carpeta Descargas.")
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")
        else:
            print("No se ha listado ningún archivo aún.")

    @staticmethod
    def simular_teclas_leer_pdf():
        keyboard.press_and_release('ctrl+shift+u')
        print("Lectura de página activada.")

    @staticmethod
    def abrir_archivo_por_nombre(nombre):
        try:
            path = os.path.expanduser("~/Downloads")
            archivos = os.listdir(path)
            for archivo in archivos:
                if nombre.lower() in archivo.lower():
                    os.startfile(os.path.join(path, archivo))
                    print(f"Archivo '{archivo}' abierto.")
                    return
            print(f"No se encontró ningún archivo que contenga '{nombre}' en el nombre.")
        except Exception as e:
            print(f"Error al abrir el archivo: {e}")
