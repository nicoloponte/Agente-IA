from langchain.tools import BaseTool

class SecurityTool(BaseTool):
    name: str = "Seguridad"
    description: str = "Útil para validar comandos peligrosos antes de ejecutarlos."

    def _run(self, command: str) -> str:
        dangerous_commands = ["rm -rf", "sudo", "format c:"]
        for dangerous_command in dangerous_commands:
            if dangerous_command in command:
                return "Comando peligroso detectado. Ejecución cancelada."
        return "Comando seguro."

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")