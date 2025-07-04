from langchain.tools import BaseTool
import speech_recognition as sr
import pyttsx3

class VoiceCommandsTool(BaseTool):
    name: str = "Comandos de voz"
    description: str = "Útil para reconocer comandos de voz y responder con voz."

    def _run(self, command: str) -> str:
        try:
            if command == "reconocer":
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return text
            elif command.startswith("hablar"):
                text = command[7:]
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                return "Texto hablado."
            else:
                return "Comando de voz no válido."
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")