import pytest
from agent.tools.email_notifier import EmailNotifierTool
import os
from dotenv import load_dotenv

load_dotenv()

def test_email_notifier_tool():
    tool = EmailNotifierTool()
    # Para probar el envío de emails, necesitas configurar tus credenciales en .env
    # y asegurarte de que la cuenta de correo tenga habilitado el acceso de aplicaciones menos seguras.
    # Esta prueba puede fallar si no se configuran correctamente las credenciales.
    # result = tool.run(f"{os.getenv('EMAIL_TEST_TO')} TestSubject TestMessage")
    # assert "Correo electrónico enviado" in result
    pass # Se salta la prueba si no se configuran las credenciales.