# main.py
import speech_recognition as sr
import pyttsx3
from agent.agent_core import JaimeAgent
import sys  # Importamos sys

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di algo...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print(f"Texto reconocido: {text}")
        return text
    except sr.UnknownValueError:
        print("No se pudo reconocer el audio.")
        return None
    except sr.RequestError as e:
        print(f"Error al solicitar resultados; {e}")
        return None

def speak(text):
    engine = pyttsx3.init()
    engine.say(text.encode('utf-8').decode('utf-8'))
    engine.runAndWait()

def main():
    agent = JaimeAgent()

    if len(sys.argv) > 1 and sys.argv[1] == '--file' and len(sys.argv) > 2:
        file_path = sys.argv[2]
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                command = file.read().strip()  # Leemos el archivo y quitamos espacios en blanco
            response = agent.run(command)
            print(f"Respuesta de Jaime: {response}")
            speak(response)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{file_path}'")
            speak(f"Error: No se encontró el archivo '{file_path}'")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            speak(f"Ocurrió un error al leer el archivo: {e}")

    else:
        while True:
            try:
                input_type = input("¿Voz (V) o Texto (T)? ").strip().lower()
                if input_type == "v":
                    command = recognize_speech()
                elif input_type == "t":
                    command = input("Introduce el comando: ").strip()
                else:
                    print("Entrada no válida.")
                    continue

                if command:
                    if "salir" in command.lower() or "adiós" in command.lower():
                        print("Saliendo del agente Jaime.")
                        speak("Adiós")
                        break  # Sale del bucle y termina el programa

                    # Nuevo comando para completar archivos con código
                    if "completar archivos" in command.lower():
                        ruta_carpeta = input("Introduce la ruta de la carpeta: ").strip()
                        prompt = input("Introduce el prompt para generar código: ").strip()
                        resultado = agent.completar_archivos_con_codigo(ruta_carpeta, prompt)
                        print(f"Resultado: {resultado}")
                        speak(resultado)
                    else:
                        # Ejecutar otros comandos
                        response = agent.run(command)
                        print(f"Respuesta de Jaime: {response}")
                        speak(response)

            except KeyboardInterrupt:
                print("\nSaliendo...")
                break

if __name__ == "__main__":
    main()