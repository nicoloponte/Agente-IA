from langchain.tools import BaseTool
import requests

class APIIntegratorTool(BaseTool):
    name: str = "Integrar API"
    description: str = "Útil para interactuar con APIs externas."

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ")
            url = parts[0]
            method = parts[1].upper()
            data = " ".join(parts[2:])

            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, data=data)
            else:
                return "Método no válido."

            return response.text
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")