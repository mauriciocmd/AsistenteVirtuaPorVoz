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
        self.dictado_activo = True
        self.en_chatgpt = False

    def activar_comandos(self):
        while not self.detener_evento.is_set():
            comando = self.reconocedor.reconocer_voz()
            if self.dictado_activo:
                self.procesar_comando_dictado(comando)
            else:
                if "empezar dictado" in comando:
                    self.empezar_dictado()
                elif "cerrar asistente virtual" in comando:
                    self.detener_evento.set()
                    Acciones.cerrar_asistente()
                    self.cerrar_app_callback()

            if self.en_chatgpt:
                if "buscar gpt" in comando:
                    self.empezar_busqueda_chatgpt()
                elif "enviar busqueda gpt" in comando:
                    self.enviar_busqueda_chatgpt()

        self.logger("Asistente de Voz detenido.")

    def procesar_comando_dictado(self, comando):
        if "abrir word" in comando:
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
        elif "terminar dictado" in comando:
            self.terminar_dictado()

    def empezar_dictado(self):
        self.dictado_activo = True
        print("Dictado iniciado. Di 'terminar dictado' para finalizar.")

    def terminar_dictado(self):
        self.dictado_activo = False
        print("Dictado terminado.")

    def empezar_busqueda_chatgpt(self):
        if self.en_chatgpt:
            PageChatGPT.activar_campo_busqueda()
            print("Activando búsqueda en ChatGPT. Empieza a dictar la consulta.")

    def enviar_busqueda_chatgpt(self):
        if self.en_chatgpt:
            consulta = self.reconocedor.empezar_dictado()
            PageChatGPT.buscar_en_chatgpt(consulta)
