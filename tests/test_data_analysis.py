import pytest
import pandas as pd
from agent.tools.data_analysis import DataAnalysisTool

def test_data_analysis_tool():
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    df.to_csv("test.csv", index=False)

    tool = DataAnalysisTool()
    result = tool.run("test.csv resumen")
    assert "count" in result