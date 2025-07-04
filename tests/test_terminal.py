import pytest
from agent.tools.terminal import TerminalTool

def test_terminal_tool():
    tool = TerminalTool()
    result = tool.run("echo 'test'")
    assert "test" in result