from langchain.tools import BaseTool
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

class EmailNotifierTool(BaseTool):
    name: str = "Enviar correo electrónico"
    description: str = "Útil para enviar correos electrónicos."

    def _run(self, command: str) -> str:
        try:
            parts = command.split(" ")
            to_email = parts[0]
            subject = parts[1]
            message = " ".join(parts[2:])

            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = os.getenv("EMAIL_USER")
            msg["To"] = to_email

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
                smtp.send_message(msg)

            return f"Correo electrónico enviado a {to_email}."
        except Exception as e:
            return str(e)

    async def _arun(self, command: str) -> str:
        raise NotImplementedError("No implementado")