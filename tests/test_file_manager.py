import pytest
import os
from agent.tools.file_manager import FileManagerTool

def test_file_manager_tool():
    tool = FileManagerTool()
    tool.run("crear test.txt")
    assert os.path.exists("test.txt")
    tool.run("escribir test.txt contenido de prueba")
    with open("test.txt", "r") as f:
        assert f.read() == "contenido de prueba"
    tool.run("eliminar test.txt")
    assert not os.path.exists("test.txt")