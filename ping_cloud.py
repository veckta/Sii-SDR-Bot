import requests
import json

url = "https://walrus-app-7dxde.ondigitalocean.app/webhook"
payload = {
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "mock_waba_id",
        "changes": [{
            "value": {
                "messaging_product": "whatsapp",
                "metadata": {"display_phone_number": "542212026568", "phone_number_id": "927495553789672"},
                "messages": [{
                    "from": "5492216146709",
                    "id": "mock_msg_id",
                    "timestamp": "16650123456",
                    "text": {"body": "Ping de diagnóstico autonomo"},
                    "type": "text"
                }]
            },
            "field": "messages"
        }]
    }]
}

try:
    print(f"Enviando POST a {url}...")
    res = requests.post(url, json=payload)
    print(f"Respuesta del servidor: {res.status_code}")
    print(f"Cuerpo: {res.text}")
except Exception as e:
    print(f"Error: {e}")
