# pageteams.py

import pyautogui
import time
import cv2
import numpy as np
import easyocr
import pygetwindow as gw
import requests
from bs4 import BeautifulSoup

class PageTeams:
    def __init__(self, engine):
        self.engine = engine
        self.ultimo_comando = ""
        self.reader = easyocr.Reader(['es'])  # Inicia el lector para el idioma español

    def hacer_click_en_imagen(self, imagen_referencia, tiempo_espera_maximo=10):
        """Busca la imagen en la pantalla y hace clic en ella si se encuentra, esperando hasta un tiempo máximo."""
        tiempo_esperado = 0
        intervalo_espera = 0.5
        img_referencia = cv2.imread(imagen_referencia)

        while tiempo_esperado < tiempo_espera_maximo:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
            resultado = cv2.matchTemplate(screenshot_bgr, img_referencia, cv2.TM_CCOEFF_NORMED)
            umbral = 0.8
            loc = np.where(resultado >= umbral)

            if loc[0].size > 0:
                for pt in zip(*loc[::-1]):  
                    x = pt[0] + img_referencia.shape[1] // 2
                    y = pt[1] + img_referencia.shape[0] // 2
                    pyautogui.click(x, y)
                    return True

            time.sleep(intervalo_espera)
            tiempo_esperado += intervalo_espera

        print(f"No encontré la imagen '{imagen_referencia}' en la pantalla después de {tiempo_espera_maximo} segundos.")
        return False

    def listar_tareas(self, categoria="Próximamente"):
        print(f"Intentando listar tareas en la categoría: {categoria}")
        try:
            if not self.hacer_click_en_imagen('botonTareasTeams.PNG'):
                print("Error al abrir el apartado de tareas.")
                return

            time.sleep(2)  
            categorias = {
                "Próximamente": 'botonProximamenteTeams.PNG',
                "Vencida": 'botonVencidasTeams.PNG',
                "Completado": 'botonCompletadasTeams.PNG'
            }
            if categoria in categorias:
                if self.hacer_click_en_imagen(categorias[categoria]):
                    time.sleep(2)
                    print("Imagen de categoría encontrada. Procediendo a leer tareas listadas.")
                    self.leer_tareas_listadas()
                else:
                    print(f"No se encontró la imagen para la categoría {categoria}.")
            else:
                print(f"No se reconoció la categoría: {categoria}")
        except Exception as e:
            print(f"Error al listar tareas de la categoría {categoria}: {e}")

    def leer_tareas_listadas(self):
        """Lee las tareas listadas en la ventana activa usando BeautifulSoup para filtrar el contenido."""
        try:
            # Obtener la URL de la ventana activa de Teams
            ventana = gw.getActiveWindow()
            if ventana:
                url = "http://teams.microsoft.com"  # URL de Teams, ajusta según sea necesario
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Filtra solo el contenido relevante de las tareas
                tareas = []
                for tarea in soup.find_all(['article', 'p', 'h1', 'h2']):
                    tareas.append(tarea.get_text(separator=" ", strip=True))

                texto_tareas = "\n".join(tareas)

                # Leer el texto usando el motor de texto a voz
                if texto_tareas:
                    print("Texto detectado:", texto_tareas)
                    self.engine.say("Las tareas listadas son:")
                    self.engine.say(texto_tareas)
                    self.engine.runAndWait()
                else:
                    print("No se detectó texto en la ventana activa.")
                    self.engine.say("No se detectó texto en la ventana activa.")
                    self.engine.runAndWait()
            else:
                print("No se pudo detectar la ventana activa.")
                self.engine.say("No se pudo detectar la ventana activa.")
                self.engine.runAndWait()
        except Exception as e:
            print(f"Error al leer tareas listadas: {e}")
            self.engine.say(f"Error al leer tareas listadas: {e}")
            self.engine.runAndWait()

    def entrar_a_tarea(self, nombre_parcial):
        """Navega hacia la tarea que coincida con el nombre parcial dado."""
        try:
            # Simular OCR en la pantalla para encontrar la tarea con el nombre parcial.
            self.engine.say(f"Buscando y entrando en la tarea con el nombre parcial {nombre_parcial}.")
            self.engine.runAndWait()
            # Aquí implementaríamos el código de reconocimiento de texto y navegación a la tarea
        except Exception as e:
            print(f"Error al intentar entrar a la tarea: {e}")
