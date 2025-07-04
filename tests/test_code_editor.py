import pytest
from agent.tools.code_editor import CodeEditorTool

def test_generate_code():
    tool = CodeEditorTool()
    query = "generar```codigo.py```print('Hola mundo')"
    result = tool._run(query)
    assert "Código generado y guardado en codigo.py" in result

def test_run_tests():
    tool = CodeEditorTool()
    query = "escribir```codigo.py```print('Hola mundo')"
    result = tool._run(query)
    assert "Pruebas:" in result

def test_analyze_code_output():
    tool = CodeEditorTool()
    query = "escribir```codigo.py```print('Hola mundo')"
    result = tool._run(query)
    assert "Salida del código:" in result
