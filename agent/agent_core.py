import re
import logging
import traceback
import os
import requests
from bs4 import BeautifulSoup
import csv  # Importamos el módulo csv para manejar archivos CSV

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from agent.debugger import Debugger
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType
from agent.tools import (
    terminal, browser, file_manager, email_notifier, api_integrator,
    voice_commands, desktop_control, web_automation, database_query,
    data_analysis, task_automation, security, test_runner, CodeEditorTool,
    csv_manager  # Importamos la nueva herramienta CSVManagerTool
)
from agent.memory import JaimeMemory
from agent.logger import JaimeLogger
from utils import load_env

class JaimeAgent:
    def __init__(self):
        print("Inicializando JaimeAgent...")
        ollama_base_url = load_env()
        self.llm = OllamaLLM(base_url=ollama_base_url, model="qwen2.5-coder:latest")
        self.memory = JaimeMemory()
        self.logger = JaimeLogger()
        self.tools = [
            terminal.TerminalTool(),
            browser.BrowserTool(),
            file_manager.FileManagerTool(),
            email_notifier.EmailNotifierTool(),
            api_integrator.APIIntegratorTool(),
            voice_commands.VoiceCommandsTool(),
            desktop_control.DesktopControlTool(),
            web_automation.WebAutomationTool(),
            database_query.DatabaseQueryTool(),
            data_analysis.DataAnalysisTool(),
            task_automation.TaskAutomationTool(),
            security.SecurityTool(),
            test_runner.TestRunnerTool(),
            CodeEditorTool(agent=self),
            csv_manager.CSVManagerTool(),  # Agregamos la nueva herramienta CSVManagerTool
        ]
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            prefix="Eres un agente de IA multifuncional, puedes hacer todo lo que te propongas.",
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=60,  # Aumenta el límite de iteraciones
            max_execution_time=600  # Aumenta el límite de tiempo (en segundos)
        )
        self.debugger = Debugger(self)

        try:
            response = self.llm.invoke("Hola, Ollama.")
            print(f"Respuesta de Ollama: {response}")
        except Exception as e:
            print(f"Error de conexión con Ollama: {e}")
        print("JaimeAgent inicializado.")

    def _process_agent_response(self, response):
        if isinstance(response, dict) and "output" in response:
            return {"output": response["output"]}
        elif isinstance(response, str):
            thought_match = re.search(r"Thought: (.*)", response)
            action_match = re.search(r"Action: (.*)", response)

            if thought_match and action_match:
                thought = thought_match.group(1).strip()
                action = action_match.group(2).strip()
                return {"thought": thought, "action": action}
            elif thought_match:
                thought = thought_match.group(1).strip()
                return {"thought": thought}
            elif action_match:
                action = action_match.group(2).strip()
                return {"action": action}
            elif "No" in response:
                return {"output": "Acción completada."}
            else:
                return {"output": response}
        else:
            return {"output": str(response)}

    def run(self, input_text, prompt=None):
        print(f"Ejecutando comando: {input_text}")
        self.logger.log(f"Input: {input_text}")
        try:
            if "hola" in input_text.lower():
                response = {"output": "Hola, como puedo ayudarte?"}
            elif "llueve" in input_text.lower() and "granada" in input_text.lower():
                search_query = "lluvia en granada"
                search_url = f"https://duckduckgo.com/?q={consulta_duckduckgo}"
                response = self.agent.invoke({"input": search_url, "tool_names": ["Navegar por la web"]})
                response = self._process_agent_response(response)
            elif "Busca en DuckDuckGo" in input_text.lower():
                consulta = input_text.split('"')[1]
                consulta_duckduckgo = consulta.replace(" ", "+")
                url = f"https://duckduckgo.com/?q={consulta_duckduckgo}"
                try:
                    respuesta = requests.get(url)
                    respuesta.raise_for_status()
                    soup = BeautifulSoup(respuesta.text, 'html.parser')
                    resultados = soup.find_all('article', class_='result')
                    datos = []
                    for resultado in resultados:
                        nombre_empresa = resultado.find('h2').text if resultado.find('h2') else "No encontrado"
                        enlace = resultado.find('a', class_='result__a')['href'] if resultado.find('a', class_='result__a') else "No encontrado"
                        texto_resultado = resultado.text
                        correo = re.search(r'[\w\.-]+@[\w\.-]+', texto_resultado)
                        correo = correo.group(0) if correo else "No encontrado"
                        instagram = re.search(r'instagram\.com/[\w\.-]+', texto_resultado)
                        instagram = instagram.group(0) if instagram else "No encontrado"
                        datos.append([nombre_empresa, correo, instagram, enlace])

                    self._generar_tabla_y_guardar(datos, "C:\contactos.txt")
                    response = {"output": "Búsqueda en DuckDuckGo completada y tabla generada."}
                except requests.exceptions.RequestException as e:
                    response = {"output": f"Error en la búsqueda en DuckDuckGo: {e}"}
            elif prompt:
                response = self.generar_codigo(prompt)
            else:
                response = self.agent.invoke(input_text)
                response = self._process_agent_response(response)

            if isinstance(response, dict) and "action" in response:
                print(f"Thought: {response.get('thought', '')}")
                print(f"Action: {response['action']}")
                self._execute_action(response['action'])
                return response['action']
            elif isinstance(response, dict) and "thought" in response:
                print(f"Thought: {response['thought']}")
                return response['thought']
            elif isinstance(response, dict) and "output" in response:
                self.logger.log(f"Output: {response['output']}")
                print(f"Respuesta del agente: {response['output']}")
                return response["output"]
            else:
                self.logger.log(f"Output: {response}")
                print(f"Respuesta del agente: {response}")
                return response

        except Exception as e:
            self.logger.log(f"Error: {e}")
            print(f"Error en la ejecución: {e}")
            tb_str = traceback.format_exc()
            debug_result = self.debugger.debug(str(e), tb_str)
            return f"Error: {e}. {debug_result}"

    def leer_archivo(self, ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                return archivo.read()
        except FileNotFoundError:
            return f"Error: Archivo no encontrado en la ruta '{ruta_archivo}'"
        except Exception as e:
            return f"Error al leer el archivo: {e}"

    def generar_codigo(self, prompt):
        try:
            response = self.llm.invoke(prompt)
            code = response["output"]
            return {"output": code}
        except Exception as e:
            return {"output": f"Error al generar código: {e}"}

    def _execute_action(self, action_string):
        if "crear" in action_string.lower():
            file_path = action_string.split("crear ")[1].strip()
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    pass
                print(f"Archivo creado: {file_path}")
            except Exception as e:
                print(f"Error al crear el archivo: {e}")

    def _generar_tabla_y_guardar(self, datos, ruta_archivo):
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("Nombre de la Empresa\tCorreo de Contacto\tInstagram\n")  # Encabezados
                for fila in datos:
                    archivo.write(f"{fila[0]}\t{fila[1]}\t{fila[2]}\n")
            print(f"Tabla guardada en: {ruta_archivo}")
        except Exception as e:
            print(f"Error al guardar la tabla: {e}")

    def leer_carpeta(self, ruta_carpeta):
        try:
            # Listar todos los archivos en la carpeta
            archivos = os.listdir(ruta_carpeta)
            return archivos
        except Exception as e:
            return f"Error al leer la carpeta: {e}"

    def identificar_archivos_a_completar(self, ruta_carpeta, extension=".py"):
        try:
            archivos = self.leer_carpeta(ruta_carpeta)
            # Filtrar archivos por extensión
            archivos_a_completar = [archivo for archivo in archivos if archivo.endswith(extension)]
            return archivos_a_completar
        except Exception as e:
            return f"Error al identificar archivos: {e}"

    def crear_estructura_proyecto(self, ruta_base):
        estructura = {
            "agent": ["__init__.py", "agent_core.py", "debugger.py", "logger.py", "memory.py"],
            "agent/tools": ["code_editor.py", "data_analysis.py", "api_integrator.py", "automation.py", "browser.py", "database_query.py", "desktop_control.py", "email.py", "file_manager.py", "docx_manager.py", "terminal.py", "email_notifier.py", "task_automation.py", "security.py", "voice_commands.py", "web_automation.py", "test_tools.py", "interaccion_aplicaciones.py"],
            "gui": ["__init__.py", "main_window.py"],
            "logs": [],
            "tests": ["test_browser.py", "test_email.py", "test_terminal.py", "test_code_editor.py", "test_data_analysis.py", "test_database_query.py", "test_desktop_control.py", "test_email_notifier.py", "test_file_manager.py", "test_security.py", "test_task_automation.py", "test_tools.py", "test_voice_commands.py", "test_web_automation.py"],
            "templates": ["index.html"]
        }

        for directorio, archivos in estructura.items():
            ruta_directorio = os.path.join(ruta_base, directorio)
            os.makedirs(ruta_directorio, exist_ok=True)
            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_directorio, archivo)
                with open(ruta_archivo, 'w') as f:
                    pass  # Crear archivo vacío
                print(f"Archivo creado: {ruta_archivo}")

    def verificar_estructura_proyecto(self, ruta_base):
        estructura = {
            "agent": ["__init__.py", "agent_core.py", "debugger.py", "logger.py", "memory.py"],
            "agent/tools": ["code_editor.py", "data_analysis.py", "api_integrator.py", "automation.py", "browser.py", "database_query.py", "desktop_control.py", "email.py", "file_manager.py", "docx_manager.py", "terminal.py", "email_notifier.py", "task_automation.py", "security.py", "voice_commands.py", "web_automation.py", "test_tools.py", "interaccion_aplicaciones.py"],
            "gui": ["__init__.py", "main_window.py"],
            "logs": [],
            "tests": ["test_browser.py", "test_email.py", "test_terminal.py", "test_code_editor.py", "test_data_analysis.py", "test_database_query.py", "test_desktop_control.py", "test_email_notifier.py", "test_file_manager.py", "test_security.py", "test_task_automation.py", "test_tools.py", "test_voice_commands.py", "test_web_automation.py"],
            "templates": ["index.html"]
        }

        for directorio, archivos in estructura.items():
            ruta_directorio = os.path.join(ruta_base, directorio)
            if not os.path.exists(ruta_directorio):
                print(f"Error: El directorio {ruta_directorio} no existe.")
                return False
            for archivo in archivos:
                ruta_archivo = os.path.join(ruta_directorio, archivo)
                if not os.path.exists(ruta_archivo):
                    print(f"Error: El archivo {ruta_archivo} no existe.")
                    return False
        return True

    def completar_archivos_con_codigo(self, ruta_carpeta, prompt, extension=".py"):
        try:
            archivos_a_completar = self.identificar_archivos_a_completar(ruta_carpeta, extension)
            for archivo in archivos_a_completar:
                ruta_archivo = os.path.join(ruta_carpeta, archivo)
                # Leer el contenido actual del archivo
                contenido_actual = self.leer_archivo(ruta_archivo)
                # Generar código adicional basado en el prompt
                respuesta = self.generar_codigo(prompt)
                if "output" in respuesta:
                    codigo_generado = respuesta["output"]
                    # Escribir el código generado en el archivo
                    with open(ruta_archivo, 'a', encoding='utf-8') as f:
                        f.write("\n" + codigo_generado)
                    print(f"Código añadido al archivo: {ruta_archivo}")
                else:
                    print(f"Error al generar código para {ruta_archivo}: {respuesta}")
            return "Archivos completados con éxito."
        except Exception as e:
            return f"Error al completar archivos: {e}"

# Ejemplo de uso
# jaime_agent = JaimeAgent()
# ruta_carpeta = "ruta/a/la/carpeta"
# prompt = "Genera una función que sume dos números."
# resultado = jaime_agent.completar_archivos_con_codigo(ruta_carpeta, prompt)
# print(resultado)