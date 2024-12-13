import pyautogui
import time
import pyttsx3


class ControlTeams:
    def __init__(self, engine):
        self.engine = engine  # Motor de voz para hablar
        self.ruta_imagenes = "imagenes/"

    def hablar(self, mensaje):
        self.engine.say(mensaje)
        self.engine.runAndWait()

    def buscar_y_clicar(self, imagen, confianza=0.8, tiempo_espera=10):
        """
        Busca una imagen en la pantalla y hace clic en ella si se encuentra.
        Espera `tiempo_espera` segundos antes de abandonar la búsqueda.
        """
        tiempo_inicial = time.time()
        while time.time() - tiempo_inicial < tiempo_espera:
            try:
                ubicacion = pyautogui.locateCenterOnScreen(
                    f"{self.ruta_imagenes}{imagen}", confidence=confianza
                )
                if ubicacion:
                    pyautogui.click(ubicacion)
                    time.sleep(3)  # Espera 3 segundos después de hacer clic
                    return True
            except pyautogui.ImageNotFoundException:
                self.hablar(f"No se encontró la imagen {imagen}.")
            time.sleep(2)  # Espera 2 segundos antes de intentar nuevamente
        return False

    def ir_a_conversacion(self, nombre_contacto):
        """
        Navega a la conversación con un contacto específico en Microsoft Teams.
        """
        self.hablar(f"Buscando la conversación con {nombre_contacto}.")

        # Paso 1: Clic en el botón de chat en el menú
        if not self.buscar_y_clicar("chatBotonEnMenu.PNG"):
            self.hablar("No se pudo encontrar el botón de chat en el menú. Continuando con el siguiente paso.")
            time.sleep(10)  # Espera antes de intentar el siguiente paso
            return

        # Paso 2: Clic en el botón de nuevo chat
        if not self.buscar_y_clicar("chatBotonNuevoChat.PNG"):
            self.hablar("No se pudo encontrar el botón de nuevo chat. Continuando con el siguiente paso.")
            time.sleep(10)  # Espera antes de intentar el siguiente paso
            return

        # Paso 3: Escribir el nombre del contacto
        pyautogui.write(nombre_contacto)
        time.sleep(3)  # Espera después de escribir el nombre
        pyautogui.press("enter")
        time.sleep(4)  # Espera después de presionar enter

        # Verificar si hay coincidencias
        try:
            sin_coincidencias = pyautogui.locateOnScreen(
                f"{self.ruta_imagenes}chatBotonSinCoincidencias.PNG", confidence=0.8
            )
            if sin_coincidencias:
                self.hablar(f"No se encontró el contacto {nombre_contacto}.")
                return
        except pyautogui.ImageNotFoundException:
            self.hablar("Contacto encontrado.")

        # Paso 4: Clic en el área para escribir mensaje
        if not self.buscar_y_clicar("chatBotonEscribirMensaje.PNG"):
            self.hablar("No se pudo encontrar el área para escribir mensajes. Finalizando operación.")
            time.sleep(10)  # Espera antes de terminar
            return

        self.hablar(f"La conversación con {nombre_contacto} está lista.")
