# asistente.py
import pyttsx3
from threading import Event
from reconocimientovoz import ReconocimientoVoz
from acciones import Acciones
from pagegpt import PageChatGPT
from lecturapdf import LecturaPDF
import time
import pyautogui
import os
import cv2
import numpy as np
from reconocimiento_intenciones import ReconocimientoIntenciones
from pageteams import PageTeams  # Asegúrate de importar la clase PageTeams
import herramientas_sistema
import clicar
from control_teams import ControlTeams



class AsistenteVoz:
    def __init__(self, logger, cerrar_app_callback, db_path='intenciones.db'):
        self.detener_evento = Event()
        self.reconocedor = ReconocimientoVoz()
        self.logger = logger
        self.cerrar_app_callback = cerrar_app_callback
        self.dictado_activo = False
        self.en_chatgpt = False

        # Crear instancia de Reconocimiento de Intenciones con los datos de la BD
        self.reconocimiento_intenciones = ReconocimientoIntenciones(db_path)

        # Inicializar el motor de voz (pyttsx3)
        self.engine = pyttsx3.init()

        # Crear instancia de PageTeams y pasarle el motor de voz
        self.page_teams = PageTeams(self.engine)
        
        self.control_teams = ControlTeams(self.engine)

    def activar_comandos(self):
        while not self.detener_evento.is_set():
            try:
                comando = self.reconocedor.reconocer_voz()
                
                if self.dictado_activo:
                    # Si el dictado está activo, procesamos el comando solo si es texto o 'terminar dictado'
                    self.procesar_dictado_texto(comando)
                else:
                    # Procesar la intención del comando
                    self.procesar_comando(comando)
                    
            except Exception as e:
                print(f"Error al reconocer voz: {e}")
        
        self.logger("Asistente de Voz detenido.")

    def procesar_dictado_texto(self, comando):
        if comando.strip() == "terminar dictado":
            self.terminar_dictado()
        elif comando:
            Acciones.escribir_texto(f"{comando} ")

    def procesar_comando(self, comando):
        # Usar el modelo entrenado para predecir la intención del comando
        intencion = self.reconocimiento_intenciones.predecir_intencion(comando.lower())
        
        # Acciones en función de la intención predicha
        if "empezar dictado" in comando:
            self.empezar_dictado()
        elif "abrir word" in comando:
            Acciones.abrir_word()
        elif comando.startswith("guardar documento word "):
            self.guardar_documento_word(comando.replace("guardar documento word ", ""))
        elif comando.lower().startswith("guardar documento pdf "):
            self.guardar_documento_pdf(comando.replace("guardar documento pdf ", ""))
        elif "abrir excel" in comando:
            Acciones.abrir_excel()
        elif "abrir powerpoint" in comando:
            Acciones.abrir_powerpoint()
        elif "abrir navegador" in comando:
            Acciones.abrir_navegador()
        elif "abrir chat gpt" in comando:
            self.abrir_chatgpt()
        elif "abrir teams" in comando:
            Acciones.abrir_teams()
            self.en_chatgpt = False
        elif "abrir pdf" in comando:
            LecturaPDF.abrir_pdf_desde_descargas()
        elif "listar archivos" in comando:
            LecturaPDF.listar_archivos()
        elif "alto listado" in comando:
            LecturaPDF.detener_listado()
        elif comando.startswith("abrir archivo "):
            LecturaPDF.abrir_archivo_por_nombre(comando.replace("abrir archivo ", ""))
        elif "leer pdf" in comando:
            LecturaPDF.simular_teclas_leer_pdf()
        elif "abrir último archivo listado" in comando:
            self.abrir_ultimo_archivo_listado()
        elif "cambiar volumen" in comando:
            herramientas_sistema.procesar_comando_volumen(comando)
        elif comando.startswith("clicar "):
            clicar.procesar_comando_clicar(comando)
        elif comando.startswith("ir a conversación con"):
            nombre_contacto = comando.replace("ir a conversación con ", "").strip()
            self.control_teams.ir_a_conversacion(nombre_contacto)
        elif comando == "enviar archivo en conversación":
            control_teams.enviar_archivo_conversacion()
        elif "cerrar asistente virtual" in comando:
            self.detener_evento.set()
            Acciones.cerrar_asistente()
            self.cerrar_app_callback()
        # Nuevos comandos para Teams
        elif "leer tareas próximas" in comando:
            self.page_teams.ejecutar_comando("leer tareas próximas")
        elif "leer tareas vencidas" in comando:
            self.page_teams.ejecutar_comando("leer tareas vencidas")
        elif "leer tareas completadas" in comando:
            self.page_teams.ejecutar_comando("leer tareas completadas")
        else:
            print(f"Comando no reconocido: {comando}")


    def empezar_dictado(self):
        if not self.dictado_activo:
            self.dictado_activo = True
            Acciones.empezar_dictado()
            print("Dictado iniciado. Di 'terminar dictado' para finalizar.")
        else:
            print("El dictado ya está activo.")

    def terminar_dictado(self):
        if self.dictado_activo:
            self.dictado_activo = False
            Acciones.terminar_dictado()
            print("Dictado terminado.")
        else:
            print("No hay dictado activo para terminar.")


    def abrir_chatgpt(self):
        Acciones.abrir_chatgpt()
        self.en_chatgpt = True
        time.sleep(5)
        PageChatGPT.activar_campo_busqueda()

    def abrir_ultimo_archivo_listado(self):
        if LecturaPDF.ultimo_archivo_listado:
            LecturaPDF.abrir_archivo_por_nombre(LecturaPDF.ultimo_archivo_listado)
        else:
            print("No hay ningún archivo listado para abrir.")

    def guardar_documento_word(self, nombre_archivo):
        try:
            # Haz clic en "Archivo"
            self.hacer_click_en_imagen('botonArchivoWord.PNG')  # Usa la imagen correspondiente
            time.sleep(1.5)  # Espera un momento adicional para que la ventana responda

            # Haz clic en "Guardar Como"
            self.hacer_click_en_imagen('botonGuardarComoWord.PNG')  # Usa la imagen correspondiente
            time.sleep(1.5)  # Espera un momento adicional para que la ventana responda

            # Busca el botón "Examinar" usando la imagen
            self.hacer_click_en_imagen('botonExaminarWord.PNG')
            time.sleep(1)  # Espera un momento para asegurarte de que se muestre la ventana

            # Navega a la carpeta de Descargas
            pyautogui.typewrite(os.path.expanduser('~') + '\\Downloads\\')  # Escribe la ruta de Descargas
            time.sleep(1)  # Espera un momento

            # Escribe el nombre del archivo
            pyautogui.typewrite(f'{nombre_archivo}.docx')
            time.sleep(1)  # Espera un momento

            # Presiona Enter para guardar
            pyautogui.press('enter')
            time.sleep(1)  # Espera un momento para asegurarte de que se guarde

            # Mensaje de éxito
            print(f"Archivo guardado en Descargas como {nombre_archivo}.docx")
        except Exception as e:
            print(f"Error al guardar el documento de Word: {e}")

    def hacer_click_en_imagen(self, imagen_referencia, tiempo_espera_maximo=10):
        """Busca la imagen en la pantalla y hace clic en ella si se encuentra, esperando hasta un tiempo máximo."""
        tiempo_esperado = 0
        intervalo_espera = 0.5  # Intervalo de espera en segundos entre intentos

        # Carga la imagen de referencia
        img_referencia = cv2.imread(imagen_referencia)

        while tiempo_esperado < tiempo_espera_maximo:
            # Toma una captura de pantalla
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)

            # Convierte la imagen de RGB a BGR
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

            # Encuentra la coincidencia
            resultado = cv2.matchTemplate(screenshot_bgr, img_referencia, cv2.TM_CCOEFF_NORMED)
            umbral = 0.8  # Ajusta el umbral según sea necesario
            loc = np.where(resultado >= umbral)

            # Si se encuentra una coincidencia, haz clic en su posición
            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):  # Cambia la ubicación para que sea (x, y)
                    # Haz clic en el centro de la imagen encontrada
                    x = pt[0] + img_referencia.shape[1] // 2
                    y = pt[1] + img_referencia.shape[0] // 2
                    pyautogui.click(x, y)
                    print(f"Hice clic en la imagen en las coordenadas ({x}, {y})")
                    return

            # Si no se encontró la imagen, esperar un tiempo antes de intentar de nuevo
            time.sleep(intervalo_espera)
            tiempo_esperado += intervalo_espera

        print(f"No encontré la imagen '{imagen_referencia}' en la pantalla después de {tiempo_espera_maximo} segundos.")
        
    def guardar_documento_pdf(self, nombre_archivo):
        try:
            # Haz clic en "Archivo"
            self.hacer_click_en_imagen('botonArchivoWord.PNG')  # Usa la imagen correspondiente
            time.sleep(1.5)  # Espera un momento adicional para que la ventana responda

            # Haz clic en "Guardar Como"
            self.hacer_click_en_imagen('botonGuardarComoWord.PNG')  # Usa la imagen correspondiente
            time.sleep(1.5)  # Espera un momento adicional para que la ventana responda

            # Busca el botón "Examinar" usando la imagen
            self.hacer_click_en_imagen('botonExaminarWord.PNG')
            time.sleep(1)  # Espera un momento para asegurarte de que se muestre la ventana

            # Navega a la carpeta de Descargas
            pyautogui.typewrite(os.path.expanduser('~') + '\\Downloads\\')  # Escribe la ruta de Descargas
            time.sleep(1)  # Espera un momento

            # Escribe el nombre del archivo con la extensión .pdf
            pyautogui.typewrite(f'{nombre_archivo}.pdf')
            time.sleep(1)  # Espera un momento

            # Haz clic en la lista desplegable de tipo
            self.hacer_click_en_imagen('tipoDocumentoGuardadoPdf.PNG')  # Usa la imagen correspondiente
            time.sleep(1)  # Espera un momento para asegurarte de que se muestre la lista

            # Selecciona "PDF (*.pdf)" de la lista
            self.hacer_click_en_imagen('tipoPdfSeleccionPdf.PNG')
            time.sleep(1)  # Espera un momento

            # Presiona Enter para seleccionar el tipo de archivo
            pyautogui.press('enter')
            time.sleep(1)  # Espera un momento para asegurarte de que se seleccione

            # Presiona Enter para guardar
            pyautogui.press('enter')
            time.sleep(1)  # Espera un momento para asegurarte de que se guarde

            # Mensaje de éxito
            print(f"Archivo guardado en Descargas como {nombre_archivo}.pdf")
        except Exception as e:
            print(f"Error al guardar el documento PDF: {e}")