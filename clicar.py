# clicar.py
import pyautogui
import pytesseract
from PIL import Image
import time

# Configurar pytesseract (asegúrate de tenerlo instalado y configurado correctamente)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Función para buscar texto y hacer clic
def clicar_texto(texto):
    try:
        # Tomar una captura de pantalla de la ventana activa
        screenshot = pyautogui.screenshot()

        # Convertir la captura de pantalla a escala de grises para mejor precisión en OCR
        gray_screenshot = screenshot.convert('L')

        # Utilizar pytesseract para obtener las posiciones del texto
        ocr_data = pytesseract.image_to_data(gray_screenshot, output_type=pytesseract.Output.DICT)

        # Buscar el texto en los datos de OCR
        for i, palabra in enumerate(ocr_data['text']):
            if texto.lower() in palabra.lower():
                # Obtener las coordenadas del texto encontrado
                x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i])
                
                # Calcular el punto central del texto para hacer clic
                centro_x = x + w // 2
                centro_y = y + h // 2

                # Mover el cursor y hacer clic
                pyautogui.moveTo(centro_x, centro_y, duration=0.2)
                pyautogui.click()
                print(f"Clic realizado en el texto: {texto}")
                return

        print(f"Texto '{texto}' no encontrado en la ventana activa.")
    except Exception as e:
        print(f"Error al buscar y clicar el texto: {e}")

# Función para procesar el comando recibido
def procesar_comando_clicar(comando):
    try:
        # Extraer el texto después de 'clicar'
        palabras = comando.lower().replace("clicar", "").strip()
        if palabras:
            clicar_texto(palabras)
        else:
            print("No se especificó ningún texto para clicar.")
    except Exception as e:
        print(f"Error procesando el comando: {e}")
