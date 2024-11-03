import os
import webbrowser
import keyboard
import pyttsx3

class Acciones:
    dictando = False  # Estado del dictado

    @staticmethod
    def abrir_word():
        try:
            os.system("start winword")
            print("Microsoft Word abierto.")
        except Exception as e:
            print(f"Error al abrir Word: {e}")

    @staticmethod
    def abrir_excel():
        try:
            os.system("start excel")
            print("Microsoft Excel abierto.")
        except Exception as e:
            print(f"Error al abrir Excel: {e}")

    @staticmethod
    def abrir_powerpoint():
        try:
            os.system("start powerpnt")
            print("Microsoft PowerPoint abierto.")
        except Exception as e:
            print(f"Error al abrir PowerPoint: {e}")

    @staticmethod
    def abrir_navegador():
        try:
            os.system("start chrome")  # Cambiar a tu navegador preferido
            print("Navegador web abierto.")
        except Exception as e:
            print(f"Error al abrir el navegador: {e}")

    @staticmethod
    def abrir_chatgpt():
        try:
            webbrowser.open("https://chatgpt.com/")
            print("ChatGPT abierto.")
        except Exception as e:
            print(f"Error al abrir ChatGPT: {e}")

    @staticmethod
    def abrir_teams():
        try:
            webbrowser.open("https://teams.microsoft.com/")
            print("Microsoft Teams abierto.")
        except Exception as e:
            print(f"Error al abrir Teams: {e}")

    @staticmethod
    def empezar_dictado():
        Acciones.dictando = True
        print("Dictado iniciado. Di 'terminar dictado' para finalizar.")

    @staticmethod
    def terminar_dictado():
        Acciones.dictando = False
        print("Dictado terminado.")

    @staticmethod
    def escribir_texto(texto):
        """
        Escribe el texto en el campo activo usando la librería keyboard.
        Verifica si el dictado está activo antes de escribir.
        """
        try:
            if Acciones.dictando and texto.strip().lower() != "terminar dictado":
                print(f"Escribiendo texto: {texto}")
                keyboard.write(texto)
            else:
                print("Dictado no está activo o se recibió el comando de finalizar.")
        except Exception as e:
            print(f"Error al escribir el texto: {e}")

    @staticmethod
    def cerrar_asistente():
        """
        Cierra el asistente con un mensaje de voz de despedida.
        """
        try:
            engine = pyttsx3.init()
            engine.say("Asistente virtual cerrado")
            engine.runAndWait()
            print("Asistente virtual cerrado")
        except Exception as e:
            print(f"Error al cerrar el asistente: {e}")
