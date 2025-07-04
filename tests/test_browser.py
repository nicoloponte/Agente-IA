import pytest
from agent.tools.browser import BrowserTool

def test_browser_tool():
    tool = BrowserTool()
    result = tool.run("https://www.google.com")
    assert "Google" in result