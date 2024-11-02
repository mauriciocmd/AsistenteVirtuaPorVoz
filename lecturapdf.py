# lecturapdf.py

import os
import tkinter as tk
from tkinter import filedialog
import webbrowser
import keyboard

class LecturaPDF:
    @staticmethod
    def abrir_pdf_desde_descargas():
        try:
            descargas_path = os.path.expanduser("~/Downloads")  # Cambiar a ~/Downloads
            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de tkinter

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
    def simular_teclas_leer_pdf():
        # Simula la combinación de teclas Ctrl + Shift + U
        keyboard.press_and_release('ctrl+shift+u')
        print("Simulación de teclas Ctrl + Shift + U realizada.")

# Ejemplo de uso
if __name__ == "__main__":
    LecturaPDF.abrir_pdf_desde_descargas()
