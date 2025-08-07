import os
import requests
import smtplib
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from email.message import EmailMessage  

from logger import log_info, log_success, log_warning, log_error

load_dotenv()

URL = 'https://www.cariverplate.com.ar/venta-de-entradas'
LAST_MATCH_FILE = 'last_match.txt'

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL") or EMAIL_USER

def fetch_latest_title():
    log_info("Obteniendo datos del sitio...")
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tag = soup.find('a', class_='titulo')
        if not a_tag:
            raise ValueError("No se encontró ningún <a class='titulo'>")

        title = a_tag.text.strip()
        clean_url = a_tag.get('href')
        parsed_url = 'https://www.cariverplate.com.ar/' + clean_url

        log_success(f"Título detectado: {title}")
        return {"url": parsed_url, "title": title}

    except Exception as e:
        log_error(f"Error al obtener título: {e}")
        return {"url": "", "title": ""}

def send_email(title):
    log_info("Enviando correo...")
    try:
        msg = EmailMessage()
        msg.set_content(f"""
🎟️ Se detectó un nuevo partido con entradas disponibles.

📌 {title['title']}
🔗 {title['url']}

Este mensaje fue generado automáticamente por el bot de River Plate.
        """)
        msg['Subject'] = '🎉 Nuevo partido disponible en la web de River'
        msg['From'] = EMAIL_USER
        msg['To'] = TO_EMAIL

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        log_success("Correo enviado correctamente ✅")
    except Exception as e:
        log_error(f"No se pudo enviar el correo: {e}")

def main():
    current_title = fetch_latest_title()
    latest_title = current_title["title"]

    if not latest_title:
        log_warning("No se pudo obtener un nuevo título. Abortando...")
        return

    try:
        with open(LAST_MATCH_FILE, 'r') as txtFile:
            last_seen_title = txtFile.read().strip()
    except FileNotFoundError:
        last_seen_title = ''

    if latest_title != last_seen_title:
        log_info("Nuevo partido detectado. Actualizando y notificando...")
        send_email(current_title)
        with open(LAST_MATCH_FILE, 'w') as file:
            file.write(latest_title)
    else:
        log_info("No hay nuevos partidos.")

if __name__ == '__main__':
    main()
