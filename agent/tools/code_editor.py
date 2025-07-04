# agent/tools/code_editor.py
import subprocess
import os
import sys
from typing import Optional, Any
from langchain.tools import BaseTool

class CodeEditorTool(BaseTool):
    name: str = "Editor de Código"
    description: str = "Eres un agente de IA capaz de autodepurarte y mejorar tu código."
    agent: Optional[Any] = None

    def __init__(self, agent=None, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent

    def _generate_and_write_file(self, filename: str, prompt: str) -> str:
        try:
            response = self.agent.llm.invoke(prompt)
            code = response.content
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(code)
            tests_output = self._run_tests()
            code_output = self._analyze_code_output(filename)
            return f"Código generado y guardado en {filename}.\nPruebas:\n{tests_output}\n\nSalida del código:\n{code_output}"
        except Exception as e:
            return f"Error al generar y guardar el código: {e}"

    def _run(self, query: str) -> str:
        try:
            filename, action, code = self._parse_query(query)
            if action == "leer":
                return self._read_file(filename)
            elif action == "escribir":
                if code is None:
                    return "Error: Contenido inválido. Debe estar entre triples comillas."
                self._write_file(filename, code)
                tests_output = self._run_tests()
                code_output = self._analyze_code_output(filename)
                return f"Pruebas:\n{tests_output}\n\nSalida del código:\n{code_output}"
            elif action == "generar":
                if self.agent is None:
                    return "Error: Agente no configurado para generar código."
                if code is None:
                    return "Error: Debe proporcionar un prompt para generar el código."
                return self._generate_and_write_file(filename, code)
            else:
                return "Acción no válida. Debe ser 'leer', 'escribir' o 'generar'."
        except ValueError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: {e}"

    def _run_tests(self):
        try:
            result = subprocess.run(["pytest", "tests/test_tools.py"], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error en las pruebas: {e.stderr}"

    def _analyze_code_output(self, filename):
        try:
            result = subprocess.run([sys.executable, filename], capture_output=True, text=True)
            if result.returncode != 0:
                return f"Error al ejecutar el código:\n{result.stderr}"
            else:
                return f"Salida del código:\n{result.stdout}"
        except FileNotFoundError:
            return f"Archivo no encontrado: {filename}"
        except Exception as e:
            return f"Error inesperado: {e}"

    def _parse_query(self, query: str):
        parts = query.split("```")
        first_line_parts = parts[0].strip().split("\n")
        filename = first_line_parts[0].strip()
        action = first_line_parts[1].strip() if len(first_line_parts) > 1 else None
        code = parts[1].strip() if len(parts) > 1 else None
        return filename, action, code

    def _read_file(self, filename: str) -> str:
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"Archivo no encontrado: {filename}"

    def _write_file(self, filename: str, code: str) -> str:
        try:
            with open(filename, "w") as f:
                f.write(code)
                return f"Archivo {filename} modificado correctamente."
        except Exception as e:
            return f"Error al escribir en {filename}: {e}"