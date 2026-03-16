import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def enviar_correo(asunto, mensaje):
    # Usamos los nombres exactos de tu archivo .env
    remitente = os.getenv("CORREO_REMITENTE")
    password = os.getenv("CONTRASENA")
    destinatario = os.getenv("CORREO_DESTINATARIO")

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        # Configuración de servidor Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False