import pyautogui
import time
import cv2
import numpy as np
import easyocr # type: ignore
import pygetwindow as gw

class PageTeams:
    def __init__(self, engine):
        self.engine = engine
        self.reader = easyocr.Reader(['es'])  # Inicia el lector

    def hacer_click_en_imagen(self, imagen_referencia, tiempo_espera_maximo=10):
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

        print(f"No encontré la imagen '{imagen_referencia}' en la pantalla.")
        return False

    def listar_tareas(self, categoria):
        categorias = {
            "Próximamente": 'botonProximamenteTeams.PNG',
            "Vencida": 'botonVencidasTeams.PNG',
            "Completado": 'botonCompletadasTeams.PNG'
        }
        if categoria in categorias:
            if self.hacer_click_en_imagen('botonTareasTeams.PNG'):
                time.sleep(2)
                if self.hacer_click_en_imagen(categorias[categoria]):
                    time.sleep(2)
                    print(f"Categoría {categoria} seleccionada. Leyendo tareas.")
                    self.leer_tareas_listadas()

    def leer_tareas_listadas(self):
        screenshot = pyautogui.screenshot()
        resultado = self.reader.readtext(np.array(screenshot))
        texto_detectado = " ".join([r[1] for r in resultado])

        if texto_detectado:
            print("Texto detectado:", texto_detectado)
            self.engine.say(f"Las tareas listadas son: {texto_detectado}")
            self.engine.runAndWait()
        else:
            print("No se detectó texto en la pantalla.")
            self.engine.say("No se detectó texto en la pantalla.")
            self.engine.runAndWait()

    def ejecutar_comando(self, comando):
        if comando == "leer tareas próximas":
            self.listar_tareas("Próximamente")
        elif comando == "leer tareas vencidas":
            self.listar_tareas("Vencida")
        elif comando == "leer tareas completadas":
            self.listar_tareas("Completado")