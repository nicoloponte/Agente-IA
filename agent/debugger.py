import re
import logging
import traceback

class Debugger:
    def __init__(self, agent):
        self.agent = agent

    def debug(self, error_message, traceback_str):
        logging.error(f"Error: {error_message}")
        logging.error(f"Traceback:\n{traceback_str}")
        """Intenta depurar el código del agente."""
        logging.info("Iniciando proceso de depuración...")
        try:
            # 1. Analizar el mensaje de error y el traceback
            logging.info(f"Mensaje de error: {error_message}")
            logging.info(f"Traceback: {traceback_str}")

            # 2. Identificar el archivo y la línea del error
            error_line = self.extract_error_line(traceback_str)
            if not error_line:
                return "No se pudo identificar la línea del error."

            # 3. Leer el código del archivo
            file_path, line_number = error_line
            code = self.agent.code_editor.run(f"{file_path}\nleer")

            # 4. Modificar el código para corregir el error
            corrected_code = self.correct_code(code, line_number, error_message)

            # 5. Escribir el código corregido en el archivo
            self.agent.code_editor.run(f"{file_path}\nescribir\n{corrected_code}")

            # 6. Ejecutar las pruebas automatizadas
            test_result = self.agent.test_runner.run("pytest tests/test_tools.py")
            logging.info(f"Resultado de las pruebas: {test_result}")

            # 7. Verificar si las pruebas pasaron
            if self.check_test_passed(test_result):
                return "Error corregido y pruebas pasadas."
            else:
                return "Error corregido, pero las pruebas fallaron."

        except Exception as e:
            logging.error(f"Error durante la depuración: {e}")
            return f"Error durante la depuración: {e}"

    def extract_error_line(self, traceback_str: str) -> tuple:
        """Extrae el archivo y la línea del error del traceback."""
        try:
            # Buscar la última línea que menciona un archivo .py
            lines = traceback_str.splitlines()
            for line in reversed(lines):
                match = re.search(r'File "([^"]+)", line (\d+),', line)
                if match:
                    file_path, line_number = match.groups()
                    return (file_path, int(line_number))
            return None
        except Exception as e:
            logging.error(f"Error al extraer la línea del error: {e}")
            return None

    def correct_code(self, code: str, line_number: int, error_message: str) -> str:
        """Genera una corrección para el código."""
        try:
            lines = code.splitlines()
            if line_number <= len(lines):
                # Ejemplo simple: agregar un comentario en la línea del error
                lines[line_number - 1] += "  # Corrección automática"
                return "\n".join(lines)
            return code
        except Exception as e:
            logging.error(f"Error al corregir el código: {e}")
            return code

    def check_test_passed(self, test_result: str) -> bool:
        """Verifica si todas las pruebas pasaron."""
        passed_match = re.search(r"(\d+) passed", test_result)
        failed_match = re.search(r"(\d+) failed", test_result)

        if passed_match and not failed_match:
            return True
        elif passed_match and failed_match:
            passed_count = int(passed_match.group(1))
            failed_count = int(failed_match.group(1))
            return failed_count == 0
        else:
            return False