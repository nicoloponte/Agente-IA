# agent/tools/desktop_control.py
import os
import json
from langchain.tools import BaseTool
import logging

logging.basicConfig(level=logging.INFO)

class DesktopControlTool(BaseTool):
    name: str = "Control de escritorio"
    description: str = """Útil para abrir aplicaciones de escritorio. Utiliza el nombre exacto de la aplicación como se define en app_config.json como Action Input.
    Por ejemplo, para abrir la calculadora, utiliza 'Action Input: calculadora'.
    Para abrir el navegador, utiliza 'Action Input: navegador'.
    Para abrir Slicer, utiliza 'Action Input: Slicer'
    Para abrir bloc de notas, utiliza 'Action Input: bloc de notas'"""

    def _run(self, command: str) -> str:
        try:
            app_name = self._parse_command(command)
            config = self._load_config()
            executable_path = self._get_executable_path(app_name, config)
            self._open_application(executable_path, app_name)
            return f"Aplicación '{app_name}' abierta."
        except Exception as e:
            logging.error(f"Error al abrir la aplicación: {e}")
            return f"Error: {e}"

    def _parse_command(self, command: str) -> str:
        parts = command.split(" ", 1)
        return parts[1].lower() if len(parts) > 1 else parts[0].lower()

    def _load_config(self) -> dict:
        config_path = "app_config.json"
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo de configuración no encontrado: {config_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Error al decodificar el archivo de configuración: {config_path}")

    def _get_executable_path(self, app_name: str, config: dict) -> str:
        if app_name not in config:
            raise ValueError(f"Aplicación '{app_name}' no encontrada en la configuración.")
        return config[app_name]

    def _open_application(self, executable_path: str, app_name:str) -> None:
        try:
            if os.name == 'nt':
                os.startfile(executable_path)
            elif os.name == 'posix':
                os.system(f"open '{executable_path}'")
            else:
                raise OSError("Sistema operativo no soportado.")
        except OSError as e:
            raise OSError(f"Error al abrir '{app_name}': {e}")

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")