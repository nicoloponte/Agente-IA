from langchain.tools import BaseTool  # Importar BaseTool desde langchain.tools
import csv
import os

class CSVManagerTool(BaseTool):
    name: str = "Gestionar CSV"
    description: str = """
    Útil para crear, leer y escribir archivos CSV.
    Los comandos deben seguir el formato:
    - crear_csv <ruta_archivo_csv> <encabezados>
    - escribir_csv <ruta_archivo_csv> <fila>
    - leer_csv <ruta_archivo_csv>
    """

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ", 2)  # Divide en máximo 3 partes
            action = parts[0].lower()

            if action == "crear_csv":
                if len(parts) < 3:
                    return "Error: Falta la ruta del archivo CSV o los encabezados."
                ruta_csv = parts[1].strip()
                encabezados = parts[2].split(",")  # Separar encabezados por comas
                # Crear directorios padres si no existen
                os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
                with open(ruta_csv, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(encabezados)
                return f"Archivo CSV creado en {ruta_csv} con los encabezados: {', '.join(encabezados)}."

            elif action == "escribir_csv":
                if len(parts) < 3:
                    return "Error: Falta la ruta del archivo CSV o la fila a escribir."
                ruta_csv = parts[1].strip()
                fila = parts[2].split(",")  # Separar valores de la fila por comas
                # Crear directorios padres si no existen
                os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
                with open(ruta_csv, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(fila)
                return f"Fila añadida al archivo CSV en {ruta_csv}."

            elif action == "leer_csv":
                if len(parts) < 2:
                    return "Error: Falta la ruta del archivo CSV."
                ruta_csv = parts[1].strip()
                if not os.path.exists(ruta_csv):
                    return f"Error: El archivo CSV {ruta_csv} no existe."
                with open(ruta_csv, mode="r", encoding="utf-8") as file:
                    reader = csv.reader(file)
                    contenido = list(reader)
                return f"Contenido del archivo CSV {ruta_csv}:\n{contenido}"

            else:
                return "Error: Acción no válida. Las acciones válidas son: crear_csv, escribir_csv, leer_csv."

        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")