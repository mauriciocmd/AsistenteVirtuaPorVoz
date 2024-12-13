import speech_recognition as sr
import time

class ReconocimientoVoz:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def reconocer_voz(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Escuchando...")
            try:
                # Ampliar tiempos para escuchar frases largas
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
                texto = self.recognizer.recognize_google(audio, language="es-ES")
                print("Has dicho:", texto)
                return texto.lower()
            except sr.WaitTimeoutError:
                print("Tiempo de espera agotado.")
                return ""
            except sr.UnknownValueError:
                print("No se pudo entender el audio")
                return ""
            except sr.RequestError as e:
                print(f"Error al solicitar resultados del servicio de reconocimiento de voz: {e}")
                return ""

    def empezar_dictado(self):
        texto = []
        print("Dictado iniciado. Di 'terminar dictado' para finalizar.")
        while True:
            palabra = self.reconocer_voz()
            if "terminar dictado" in palabra:
                print("Dictado terminado.")
                return " ".join(texto)
            elif palabra:
                texto.append(palabra)
            # Pausa corta para evitar cortes rápidos
            time.sleep(1)

    def ejecutar_comando(self, comando):
        if comando == "empezar dictado":
            resultado_dictado = self.empezar_dictado()
            print("Resultado del dictado:", resultado_dictado)
        elif comando == "cerrar asistente virtual":
            print("Cerrando el asistente virtual...")
            exit()
        else:
            print("Comando no reconocido:", comando)

    def main(self):
        print("Asistente virtual iniciado. Di 'empezar dictado' para empezar a dictar.")
        while True:
            comando = self.reconocer_voz()
            if comando:
                self.ejecutar_comando(comando)
            # Retraso adicional entre comandos
            time.sleep(2)

if __name__ == "__main__":
    rv = ReconocimientoVoz()
    rv.main()
