import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import pyttsx3

class LectorVoz:
    @staticmethod
    def leer_pagina_web(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica que la solicitud fue exitosa

            content_type = response.headers.get('Content-Type')
            if 'application/pdf' in content_type:
                LectorVoz.leer_pdf(url)
            else:
                LectorVoz.leer_html(response.text)

        except Exception as e:
            print(f"Error al leer la página web: {e}")

    @staticmethod
    def leer_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        LectorVoz.leer_texto(text)

    @staticmethod
    def leer_pdf(url):
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open("temp.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)

            doc = fitz.open("temp.pdf")
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()

            LectorVoz.leer_texto(text)

        except Exception as e:
            print(f"Error al leer el PDF: {e}")

    @staticmethod
    def leer_texto(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
