import os
import webbrowser
import keyboard
import pyttsx3

class Acciones:
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

    dictando = False

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
        if Acciones.dictando:
            keyboard.write(texto)

    @staticmethod
    def cerrar_asistente():
        engine = pyttsx3.init()
        engine.say("Asistente virtual cerrado")
        engine.runAndWait()
        print("Asistente virtual cerrado")









# import os
# import webbrowser
# import keyboard
# import pyttsx3

# def abrir_word():
#     try:
#         os.system("start winword")
#     except Exception as e:
#         print(f"Error al abrir Word: {e}")

# def abrir_excel():
#     try:
#         os.system("start excel")
#     except Exception as e:
#         print(f"Error al abrir Excel: {e}")

# def abrir_powerpoint():
#     try:
#         os.system("start powerpnt")
#     except Exception as e:
#         print(f"Error al abrir PowerPoint: {e}")

# def abrir_navegador():
#     try:
#         os.system("start chrome")  # Cambiar a tu navegador preferido
#     except Exception as e:
#         print(f"Error al abrir el navegador: {e}")

# def abrir_chatgpt():
#     try:
#         webbrowser.open("https://chatgpt.com/")
#     except Exception as e:
#         print(f"Error al abrir ChatGPT: {e}")

# def abrir_teams():
#     try:
#         webbrowser.open("https://teams.microsoft.com/")
#     except Exception as e:
#         print(f"Error al abrir Teams: {e}")

# # Variable global para controlar el dictado
# dictando = False

# def empezar_dictado():
#     global dictando
#     dictando = True
#     print("Dictado iniciado. Di 'terminar dictado' para finalizar.")

# def terminar_dictado():
#     global dictando
#     dictando = False
#     print("Dictado terminado.")

# def escribir_texto(texto):
#     if dictando:
#         keyboard.write(texto)

# def cerrar_asistente():
#     engine = pyttsx3.init()
#     engine.say("Asistente virtual cerrado")
#     engine.runAndWait()
#     print("Asistente virtual cerrado")





# import os
# import webbrowser
# import keyboard
# import pyttsx3

# def abrir_word():
#     os.system("start winword")

# def abrir_excel():
#     os.system("start excel")

# def abrir_powerpoint():
#     os.system("start powerpnt")

# def abrir_navegador():
#     os.system("start chrome")  # Cambiar a tu navegador preferido

# def abrir_chatgpt():
#     webbrowser.open("https://chatgpt.com/")

# def abrir_teams():
#     webbrowser.open("https://teams.microsoft.com/")

# # Variable global para controlar el dictado
# dictando = False

# def empezar_dictado():
#     global dictando
#     dictando = True

# def terminar_dictado():
#     global dictando
#     dictando = False

# def escribir_texto(texto):
#     if dictando:
#         keyboard.write(texto)

# def cerrar_asistente():
#     engine = pyttsx3.init()
#     engine.say("Asistente virtual cerrado")
#     engine.runAndWait()


'''import webbrowser
import os

def realizar_accion(intencion, comando):
    if intencion == "buscar":
        buscar_internet(comando)
    elif intencion == "crear_documento":
        crear_documento()
    elif intencion == "leer_documento":
        leer_documento()
    elif intencion == "navegar_internet":
        abrir_navegador()
    elif intencion == "control_basico":
        control_basico(comando)
    else:
        print("Intención no reconocida")

def buscar_internet(comando):
    query = comando.replace("buscar", "").strip()
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def crear_documento():
    os.system("start winword")

def leer_documento():
    os.system("start excel")

def abrir_navegador():
    webbrowser.open("https://www.google.com")

def control_basico(comando):
    if "subir volumen" in comando:
        os.system("nircmd.exe changesysvolume 2000")
    elif "bajar volumen" in comando:
        os.system("nircmd.exe changesysvolume -2000")
    elif "conectar wifi" in comando:
        os.system("netsh interface set interface 'Wi-Fi' enabled")
    elif "desconectar wifi" in comando:
        os.system("netsh interface set interface 'Wi-Fi' disabled")
'''