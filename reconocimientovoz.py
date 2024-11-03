import speech_recognition as sr

class ReconocimientoVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def reconocer_voz(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Escuchando...")
            audio = self.recognizer.listen(source)

        try:
            texto = self.recognizer.recognize_google(audio, language="es-ES")
            print("Has dicho:", texto)
            return texto.lower()
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
            return ""
        except sr.RequestError as e:
            print(f"Error al solicitar resultados del servicio de reconocimiento de voz: {e}")
            return ""

    def empezar_dictado(self):
        texto = ""
        while True:
            palabra = self.reconocer_voz()
            if palabra == "terminar dictado":
                print("Dictado terminado.")
                return texto
            texto += palabra + " "

    def ejecutar_comando(self, comando):
        if comando == "empezar dictado":
            return self.empezar_dictado()
        elif comando == "terminar dictado":
            return None  # No se ejecuta ningún comando al terminar el dictado
        elif comando == "cerrar asistente virtual":
            print("Cerrando el asistente virtual...")
            exit()
        else:
            print("Comando no reconocido:", comando)
            return None

    def main(self):
        print("Asistente virtual iniciado. Di 'empezar dictado' para empezar a dictar.")
        while True:
            comando = self.reconocer_voz()
            resultado = self.ejecutar_comando(comando)
            if resultado is not None:
                print("Resultado del dictado:", resultado)

if __name__ == "__main__":
    rv = ReconocimientoVoz()
    rv.main()
