import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID", "")
NUMERO = "54221156146709"

url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Intentar enviar un mensaje de TEXTO en lugar de plantilla
payload = {
    "messaging_product": "whatsapp",
    "to": NUMERO,
    "type": "text",
    "text": {
        "body": "Soy el bot probando texto plano."
    }
}

print("Enviando mensaje de texto de diagnóstico...")
res = requests.post(url, headers=headers, json=payload)
print(f"Status: {res.status_code}")
print(f"Respuesta completa: {res.json()}")
