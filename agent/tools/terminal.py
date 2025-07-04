from langchain.tools import BaseTool
import subprocess

class TerminalTool(BaseTool):
    name: str = "Ejecutar comando en terminal"
    description: str = "Útil para ejecutar comandos en la terminal."

    def _run(self, command: str) -> str:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")