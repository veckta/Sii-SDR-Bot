import requests
import json
import time

URL = "https://walrus-app-7dxde.ondigitalocean.app/webhook"

# Simulamos el payload de Meta para un mensaje de texto "Hola! Tengo un problema"
payload = {
    "object": "whatsapp_business_account",
    "entry": [
        {
            "id": "1234567890",
            "changes": [
                {
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": "1234567890",
                            "phone_number_id": "1234567890"
                        },
                        "contacts": [
                            {
                                "profile": {
                                    "name": "Usuario Test"
                                },
                                "wa_id": "5492215555555"
                            }
                        ],
                        "messages": [
                            {
                                "from": "5492215555555",
                                "id": "wamid.HBgLNTQ5Mj...",
                                "timestamp": str(int(time.time())),
                                "text": {
                                    "body": "Hola! Tengo un problema y necesito ayuda con mi termo"
                                },
                                "type": "text"
                            }
                        ]
                    },
                    "field": "messages"
                }
            ]
        }
    ]
}

print(f"Enviando mensaje de prueba a: {URL}")
try:
    response = requests.post(URL, json=payload, timeout=15)
    print(f"Código de respuesta HTTP: {response.status_code}")
    print(f"Respuesta del servidor: {response.text}")
except Exception as e:
    print(f"Error al conectar: {e}")
