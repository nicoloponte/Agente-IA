from langchain.tools import BaseTool
import sqlite3

class DatabaseQueryTool(BaseTool):
    name: str = "Consultar base de datos"
    description: str = "Útil para consultar bases de datos SQL."

    def _run(self, query: str) -> str:
        try:
            conn = sqlite3.connect("jaime.db")
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return str(result)
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")