from langchain.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

class WebAutomationTool(BaseTool):
    name: str = "Automatización web"
    description: str = "Útil para automatizar tareas en la web. Puede extraer texto y escribir en elementos."

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ")
            url = parts[0]
            action = parts[1]
            element_id = parts[2] if len(parts) > 2 else None
            text = " ".join(parts[3:]) if len(parts) > 3 else None

            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if action == "escribir" and element_id and text:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, element_id))
                )
                element.send_keys(text)
                driver.quit()
                return f"Texto '{text}' escrito en el elemento con ID '{element_id}'."
            elif action == "extraer_texto":
                # Extraer todo el texto visible
                all_text = soup.get_text(separator='\n', strip=True)
                driver.quit()
                return all_text
            else:
                driver.quit()
                return "Acción no válida o faltan argumentos."
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")