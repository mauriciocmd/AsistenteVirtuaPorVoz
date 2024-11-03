from threading import Event
from reconocimientovoz import ReconocimientoVoz
from acciones import Acciones
from pagegpt import PageChatGPT
from lecturapdf import LecturaPDF  # Importar LecturaPDF
import time

class AsistenteVoz:
    def __init__(self, logger, cerrar_app_callback):
        self.detener_evento = Event()
        self.reconocedor = ReconocimientoVoz()
        self.logger = logger
        self.cerrar_app_callback = cerrar_app_callback
        self.dictado_activo = False  # Inicialmente en False
        self.en_chatgpt = False

    def activar_comandos(self):
        while not self.detener_evento.is_set():
            comando = self.reconocedor.reconocer_voz()
            
            if self.dictado_activo:
                # Si el dictado está activo, procesamos solo el dictado
                self.procesar_dictado_texto(comando)
            else:
                # Si el dictado no está activo, procesamos solo comandos
                self.procesar_comando(comando)

        self.logger("Asistente de Voz detenido.")

    def procesar_dictado_texto(self, comando):
        """Procesa el texto dictado cuando el dictado está activo."""
        if comando.strip() == "terminar dictado":
            self.terminar_dictado()
        elif comando:  # Solo escribir si comando no está vacío
            Acciones.escribir_texto(comando + " ")

    def procesar_comando(self, comando):
        """Procesa los comandos cuando el dictado está desactivado."""
        if "empezar dictado" in comando:
            self.empezar_dictado()
        elif "abrir word" in comando:
            Acciones.abrir_word()
        elif "abrir excel" in comando:
            Acciones.abrir_excel()
        elif "abrir powerpoint" in comando:
            Acciones.abrir_powerpoint()
        elif "abrir navegador" in comando:
            Acciones.abrir_navegador()
        elif "abrir chat gpt" in comando:
            Acciones.abrir_chatgpt()
            self.en_chatgpt = True
            time.sleep(5)  # Esperar a que se abra ChatGPT
            PageChatGPT.activar_campo_busqueda()
        elif "abrir teams" in comando:
            Acciones.abrir_teams()
            self.en_chatgpt = False
        elif "abrir pdf" in comando:  # Añadir el comando para abrir PDF
            LecturaPDF.abrir_pdf_desde_descargas()
        elif "leer pdf" in comando:
            LecturaPDF.simular_teclas_leer_pdf()
        elif "cerrar asistente virtual" in comando:
            self.detener_evento.set()
            Acciones.cerrar_asistente()
            self.cerrar_app_callback()
        else:
            print(f"Comando no reconocido: {comando}")

    def empezar_dictado(self):
        """Activa el modo dictado."""
        self.dictado_activo = True
        Acciones.empezar_dictado()
        print("Dictado iniciado. Di 'terminar dictado' para finalizar.")

    def terminar_dictado(self):
        """Desactiva el modo dictado y vuelve al modo de comando."""
        self.dictado_activo = False
        Acciones.terminar_dictado()
        print("Dictado terminado.")

    def empezar_busqueda_chatgpt(self):
        """Activa el campo de búsqueda en ChatGPT para comenzar a dictar una consulta."""
        if self.en_chatgpt:
            PageChatGPT.activar_campo_busqueda()
            print("Activando búsqueda en ChatGPT. Empieza a dictar la consulta.")

    def enviar_busqueda_chatgpt(self):
        """Envía la búsqueda en ChatGPT basada en el dictado actual."""
        if self.en_chatgpt:
            consulta = self.reconocedor.empezar_dictado()
            PageChatGPT.buscar_en_chatgpt(consulta)
