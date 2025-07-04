from langchain.tools import BaseTool
import os

class FileManagerTool(BaseTool):
    name: str = "Gestionar archivos"
    description: str = """
    Útil para crear, leer, escribir y eliminar archivos y directorios.
    Los comandos deben seguir el formato:
    - crear <ruta_archivo_o_directorio>
    - leer <ruta_archivo>
    - escribir <ruta_archivo> <contenido>
    - eliminar <ruta_archivo_o_directorio>
    """

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ", 2)  # Divide en máximo 3 partes
            action = parts[0].lower()
            path = parts[1]

            if action == "crear":
                # Si la ruta termina con una barra, es un directorio
                if path.endswith("/") or path.endswith("\\"):
                    os.makedirs(path, exist_ok=True)
                    return f"Directorio {path} creado."
                else:
                    # Crear directorios padres si no existen
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with open(path, "w") as f:
                        pass  # Crear archivo vacío
                    return f"Archivo {path} creado."

            elif action == "leer":
                if not os.path.exists(path):
                    return f"Error: {path} no existe."
                if os.path.isdir(path):
                    return f"Error: {path} es un directorio, no se puede leer."
                with open(path, "r") as f:
                    return f.read()

            elif action == "escribir":
                if len(parts) < 3:
                    return "Error: Falta el contenido para escribir."
                content = parts[2]
                # Crear directorios padres si no existen
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w") as f:
                    f.write(content)
                return f"Contenido escrito en {path}."

            elif action == "eliminar":
                if not os.path.exists(path):
                    return f"Error: {path} no existe."
                if os.path.isdir(path):
                    os.rmdir(path)
                    return f"Directorio {path} eliminado."
                else:
                    os.remove(path)
                    return f"Archivo {path} eliminado."

            else:
                return "Error: Acción no válida. Las acciones válidas son: crear, leer, escribir, eliminar."

        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")