import pytest
from agent.tools.task_automation import TaskAutomationTool

def test_task_automation_tool():
    tool = TaskAutomationTool()
    result = tool.run("esperar 1")
    assert "Esperando 1 segundos" in result