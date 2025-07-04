from langchain.tools import BaseTool
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

class BrowserTool(BaseTool):
    name: str = "Navegar por la web"
    description: str = "Útil para navegar por la web y extraer texto de una página."

    def _run(self, url: str) -> str:
        try:
            options = Options()
            options.headless = True
            driver = webdriver.Firefox(options=options)
            driver.get(url)

            content = driver.page_source
            driver.quit()

            soup = BeautifulSoup(content, "html.parser")

            # Extraer todo el texto visible
            all_text = soup.get_text(separator='\n', strip=True)

            return all_text
        except Exception as e:
            return str(e)

    async def _arun(self, url: str) -> str:
        raise NotImplementedError("No implementado")