# tests/test_tools.py
import pytest
from agent.tools import browser, code_editor, file_manager

def test_code_editor_tool_error():
    """Prueba el manejo de errores de CodeEditorTool."""
    tool = code_editor.CodeEditorTool()
    try:
        result = tool.run("archivo_inexistente.py\nleer")
        print(f"Resultado de code_editor.CodeEditorTool: {result}")  # Agregado
        assert "archivo no encontrado" in result.lower()
    except Exception as e:
        print(f"Excepción capturada: {e}")  # Agregado
        assert False, f"Excepción inesperada: {e}" # Agregado

def test_file_manager_tool_error():
    """Prueba el manejo de errores de FileManagerTool."""
    tool = file_manager.FileManagerTool()
    result = tool.run("leer archivo_inexistente.txt")
    assert "no existe" in result.lower()