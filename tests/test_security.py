import pytest
from agent.tools.security import SecurityTool

def test_security_tool():
    tool = SecurityTool()
    result = tool.run("rm -rf /")
    assert "Comando peligroso" in result