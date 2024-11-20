# asistente.py

from threading import Event
from reconocimientovoz import ReconocimientoVoz
from acciones import Acciones
from pagegpt import PageChatGPT
from lecturapdf import LecturaPDF  
import time
import pyautogui  # Asegúrate de tener esta librería instalada
import os
import cv2
import numpy as np

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
        elif comando.startswith("guardar documento word "):
            nombre_archivo = comando.replace("guardar documento word ", "")
            self.guardar_documento_word(nombre_archivo)
        elif comando.lower().startswith("guardar documento pdf "):
            nombre_archivo = comando.replace("guardar documento pdf ", "")
            self.guardar_documento_pdf(nombre_archivo)
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
        elif "listar archivos" in comando:
            LecturaPDF.listar_archivos()
        elif "alto listado" in comando:
            LecturaPDF.detener_listado()
        elif comando.startswith("abrir archivo "):
            nombre = comando.replace("abrir archivo ", "")
            LecturaPDF.abrir_archivo_por_nombre(nombre)
        elif "leer pdf" in comando:
            LecturaPDF.simular_teclas_leer_pdf()
        elif "abrir último archivo listado" in comando:  # Nuevo comando para abrir el último archivo listado
            if LecturaPDF.ultimo_archivo_listado:
                LecturaPDF.abrir_archivo_por_nombre(LecturaPDF.ultimo_archivo_listado)
            else:
                print("No hay ningún archivo listado para abrir.")
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
