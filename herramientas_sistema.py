#herramientas_sistema.py
from word2number import w2n
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Función para cambiar el volumen del sistema
def cambiar_volumen(valor):
    try:
        # Obtener los dispositivos de audio
        dispositivos = AudioUtilities.GetSpeakers()
        interface = dispositivos.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volumen = interface.QueryInterface(IAudioEndpointVolume)

        # Asegurarse de que el valor esté dentro del rango 0-100
        porcentaje = max(0, min(100, valor)) / 100.0

        # Cambiar el volumen
        volumen.SetMasterVolumeLevelScalar(porcentaje, None)
        print(f"Volumen ajustado al {valor}%")
    except Exception as e:
        print(f"Error al cambiar el volumen: {e}")

# Función para procesar el comando recibido
def procesar_comando_volumen(comando):
    try:
        # Extraer el número del comando
        palabras = comando.lower().replace("cambiar volumen", "").strip()
        if palabras.isdigit():
            numero = int(palabras)
        else:
            numero = w2n.word_to_num(palabras)

        # Cambiar el volumen al número extraído
        cambiar_volumen(numero)
    except ValueError:
        print("No se pudo reconocer el número en el comando.")
    except Exception as e:
        print(f"Error procesando el comando: {e}")
