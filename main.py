# main.py
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from threading import Thread
from asistente import AsistenteVoz
import sys
from BD_intenciones import BaseDatosIntenciones  # importar la clase de la base de datos

class AplicacionAsistente:
    
    
        
    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Asistente de Voz")
        self.ventana.geometry("900x500")
        self.ventana.config(bg="#F5F5F5")

        # Título
        self.label = tk.Label(
            self.ventana,
            text="Asistente de Voz - USB",
            font=("Helvetica", 18, "bold"),
            bg="#F5F5F5",
            fg="#34495E"
        )
        self.label.pack(pady=10)

        # Consola con barra de desplazamiento
        self.consola_texto = ScrolledText(
            self.ventana,
            height=15,
            width=70,
            wrap=tk.WORD,
            bg="#F2F4F4",
            fg="#34495E",
            font=("Arial", 10),
            state=tk.DISABLED  # Evitar edición manual
        )
        self.consola_texto.pack(pady=10)

        # Frame de botones
        self.frame_botones = tk.Frame(self.ventana, bg="#F5F5F5")
        self.frame_botones.pack(pady=10)

        boton_color = "#2980B9"
        boton_texto = "#FFFFFF"

        botones = [
            ("Empezar dictado", self.funcion_boton_2),
            ("Terminar dictado", self.funcion_boton_3),
            ("Listar archivos", self.funcion_boton_1),
            ("Alto listado", lambda: self.asistente.procesar_comando("alto listado")),
            ("Abrir último documento listado", self.funcion_boton_4),
        ]

        for i, (texto, comando) in enumerate(botones):
            tk.Button(
                self.frame_botones,
                text=texto,
                command=comando,
                bg=boton_color,
                fg=boton_texto,
                font=("Helvetica", 10, "bold"),
                width=15
            ).grid(row=0, column=i, padx=5, pady=5)

        # Campo de texto y botón para enviar
        self.frame_entrada = tk.Frame(self.ventana, bg="#F5F5F5")
        self.frame_entrada.pack(pady=10)

        self.campo_texto = tk.Entry(self.frame_entrada, font=("Arial", 12), width=50)
        self.campo_texto.grid(row=0, column=0, padx=5)

        self.boton_enviar = tk.Button(
            self.frame_entrada,
            text="Enviar",
            command=self.procesar_texto_manual,
            bg=boton_color,
            fg=boton_texto,
            font=("Helvetica", 10, "bold")
        )
        self.boton_enviar.grid(row=0, column=1)

        # Vincula la tecla "Enter" para enviar el texto
        self.ventana.bind("<Return>", lambda event: self.procesar_texto_manual())

        self.asistente = AsistenteVoz(self.actualizar_consola, self.cerrar)
        self.iniciar_escucha()

        """ self.crear_base_datos() """
        self.ver_intenciones()
        
        # Crear base de datos y agregar intenciones al iniciar

    """ def crear_base_datos(self):
        bd = BaseDatosIntenciones()
        bd.insertar_intencion("empezar dictado", "iniciar dictado")
        bd.insertar_intencion("abrir word", "abrir documento word")
        bd.insertar_intencion("guardar documento word", "guardar word")
        bd.insertar_intencion("guardar documento pdf", "guardar pdf")
        bd.insertar_intencion("abrir excel", "abrime excel")
        bd.insertar_intencion("abrir powerpoint", "abre powerpoint")
        bd.insertar_intencion("abrir navegador", "abre el navegador")
        bd.insertar_intencion("abrir chat gpt", "abrir chat gpt")
        bd.insertar_intencion("abrir teams", "abre teams")
        bd.insertar_intencion("abrir pdf", "abrir documento pdf")
        bd.insertar_intencion("listar archivos", "lista mis archivos")
        bd.insertar_intencion("alto listado", "alto lista")
        bd.insertar_intencion("leer pdf", "lee el pdf")
        bd.insertar_intencion("abrir último archivo listado", "abril ultimo archivo listado")
        bd.insertar_intencion("cerrar asistente virtual", "cierra el asistente virtual")
        bd.insertar_intencion("terminar dictado", "terminar dictado")
        bd.insertar_intencion("terminar dictado", "terminal dictado")
        bd.cerrar_conexion() """
    
    def ver_intenciones(self):
    # Crear la base de datos e insertar intenciones si no existe
        bd = BaseDatosIntenciones()
        intenciones = bd.obtener_intenciones()  # Obtiene todas las intenciones de la base de datos
        bd.cerrar_conexion()

        # Mostrar las intenciones en la consola
        print("Lista de intenciones en la base de datos:")
        for intencion in intenciones:
            id_intencion, comando, comando_aproximado = intencion
            print(f"ID: {id_intencion}, Comando: {comando}, Comando Aproximado: {comando_aproximado}")


    def actualizar_consola(self, mensaje):
        """Actualiza el ScrolledText con el texto acumulado."""
        self.consola_texto.config(state=tk.NORMAL)  # Permitir edición temporal
        self.consola_texto.insert(tk.END, mensaje + "\n")
        self.consola_texto.see(tk.END)  # Desplaza automáticamente al final
        self.consola_texto.config(state=tk.DISABLED)  # Evitar edición manual

    def iniciar_escucha(self):
        """Inicia el hilo del asistente."""
        self.hilo_asistente = Thread(target=self.asistente.activar_comandos, daemon=True)
        self.hilo_asistente.start()

    def cerrar(self):
        """Cierra la aplicación de manera segura."""
        self.asistente.detener_evento.set()
        self.ventana.after(500, self.ventana.destroy)

    def procesar_texto_manual(self):
        """Procesa el texto ingresado en el campo como un comando de voz."""
        texto = self.campo_texto.get().strip()
        if texto:
            self.actualizar_consola(f"Tú: {texto}")
            self.campo_texto.delete(0, tk.END)  # Limpia el campo de texto
            self.asistente.procesar_comando(texto)  # Procesa el texto como comando

    # Métodos para botones
    def funcion_boton_1(self):
        self.asistente.procesar_comando("listar archivos")

    def funcion_boton_2(self):
        self.asistente.procesar_comando("empezar dictado")

    def funcion_boton_3(self):
        self.asistente.procesar_comando("terminar dictado")

    def funcion_boton_4(self):
        self.asistente.procesar_comando("abrir último archivo listado")

class RedirectOutput:
    """Clase para redirigir stdout y stderr al Label."""
    def __init__(self, callback):
        self.callback = callback

    def write(self, text):
        if text.strip():  # Ignora líneas vacías
            self.callback(text)

    def flush(self):
        pass  # Necesario para evitar errores de búfer

def main():
    root = tk.Tk()
    app = AplicacionAsistente(root)

    sys.stdout = RedirectOutput(app.actualizar_consola)
    sys.stderr = RedirectOutput(app.actualizar_consola)

    root.protocol("WM_DELETE_WINDOW", app.cerrar)
    root.mainloop()

if __name__ == "__main__":
    main()
