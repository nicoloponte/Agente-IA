import pytest
from agent.tools.api_integrator import APIIntegratorTool

def test_api_integrator_tool():
    tool = APIIntegratorTool()
    result = tool.run("https://jsonplaceholder.typicode.com/todos/1 GET")
    assert "userId" in result