import pyautogui
import time
from reconocimientovoz import ReconocimientoVoz  # Importar la clase ReconocimientoVoz

class PageChatGPT:
    @staticmethod
    def buscar_en_chatgpt(consulta):
        try:
            pyautogui.write(consulta, interval=0.1)  # Escribir la consulta con un intervalo de 0.1 segundos entre caracteres
            pyautogui.press("enter")  # Presionar Enter para enviar la consulta
            print("Consulta enviada a ChatGPT.")
        except Exception as e:
            print(f"Error al buscar en ChatGPT: {e}")

    @staticmethod
    def activar_campo_busqueda():
        try:
            ruta_imagen = "enviar_mensaje_chatgpt.png"
            print(f"Buscando la imagen en la ruta: {ruta_imagen}")

            # Ajustar la confianza
            ubicacion = pyautogui.locateCenterOnScreen(ruta_imagen, confidence=0.8)
            if ubicacion is not None:
                x, y = ubicacion
                pyautogui.click(x, y)  # Hacer clic en el texto para activar el campo de búsqueda
                print("Campo de búsqueda en ChatGPT activado.")
                PageChatGPT.empezar_transcripcion()  # Llamar a la función para empezar la transcripción
            else:
                print("No se encontró la imagen en la pantalla.")
        except FileNotFoundError:
            print(f"Archivo de imagen no encontrado: {ruta_imagen}")
        except Exception as e:
            print(f"Error al activar campo de búsqueda en ChatGPT: {e}")

    @staticmethod
    def empezar_transcripcion():
        reconocedor = ReconocimientoVoz()  # Crear una instancia de ReconocimientoVoz
        print("Empezando transcripción en ChatGPT. Empieza a dictar la consulta.")
        texto = reconocedor.empezar_dictado()  # Empezar la transcripción
        PageChatGPT.buscar_en_chatgpt(texto)  # Buscar el texto transcrito en ChatGPT
