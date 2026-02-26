import os
import requests
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID") # Debería ser el nuevo: 927495553789672

print(f"=== DIAGNÓSTICO DE SALIDA META ===")
print(f"Usando PHONE_NUMBER_ID: {PHONE_NUMBER_ID}")

# El número de Ariel registrado en el código fuente anterior
numero_destino = "5492216146709" 

url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
headers = {
    "Authorization": f"Bearer {WHATSAPP_TOKEN}",
    "Content-Type": "application/json"
}
payload = {
    "messaging_product": "whatsapp",
    "to": numero_destino,
    "type": "text",
    "text": {"body": "Hola Ariel, este es un texto de diagnóstico forzado desde el servidor usando el nuevo número oficial."}
}

res = requests.post(url, headers=headers, json=payload)
print(f"Status Code: {res.status_code}")
print(f"Respuesta de Meta: {res.text}")
