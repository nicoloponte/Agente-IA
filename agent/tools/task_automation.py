from langchain.tools import BaseTool
import time

class TaskAutomationTool(BaseTool):
    name: str = "Automatización de tareas"
    description: str = "Útil para automatizar tareas repetitivas."

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ")
            action = parts[0]

            if action == "esperar":
                seconds = int(parts[1])
                time.sleep(seconds)
                return f"Esperando {seconds} segundos."
            elif action == "repetir":
                count = int(parts[1])
                task = " ".join(parts[2:])
                result = ""
                for _ in range(count):
                    result += f"{task}\n"
                return result
            else:
                return "Acción no válida."
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")