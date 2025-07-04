from langchain.tools import BaseTool
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

class DataAnalysisTool(BaseTool):
    name: str = "Análisis de datos"
    description: str = "Útil para analizar datos y generar visualizaciones."

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ")
            file_path = parts[0]
            action = parts[1]

            df = pd.read_csv(file_path)

            if action == "resumen":
                return df.describe().to_string()
            elif action == "graficar":
                column = parts[2]
                plt.figure()
                df[column].plot()
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode()
                plt.close()
                return f'<img src="data:image/png;base64,{image_base64}" alt="Gráfico">'
            else:
                return "Acción no válida."
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")