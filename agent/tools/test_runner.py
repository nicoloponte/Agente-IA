# agent/tools/test_runner.py
import subprocess
from langchain.tools import BaseTool

class TestRunnerTool(BaseTool):
    name: str = "Ejecutor de Pruebas"
    description: str = "Útil para ejecutar pruebas automatizadas."

    def _run(self, query: str) -> str:
        try:
            result = subprocess.run(["pytest", "tests/test_tools.py", "-v"], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error en las pruebas: {e.stdout}\n{e.stderr}"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("No implementado")