import requests
import json
import time
import os

WEBHOOK_URL = "http://127.0.0.1:8000/webhook"
LOG_FILE = "app_console.log"

def probar_bot():
    print("\n🚀 INICIANDO PRUEBA DE FUEGO: SII ULTRA+ 🛡️")
    
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "messages": [{
                        "from": "5492216146709",
                        "type": "text",
                        "text": {"body": "Hola, mi heladera no enfría bien."}
                    }]
                },
                "field": "messages"
            }]
        }]
    }

    print(f"1. Enviando mensaje: 'Hola, mi heladera no enfría bien.'")
    try:
        res = requests.post(WEBHOOK_URL, json=payload)
        print(f"2. Respuesta del servidor: {res.status_code}")
        
        print("3. Esperando respuesta de OpenAI gpt-4o-mini...")
        time.sleep(5)
        
        print("4. Verificando logs...")
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lineas = f.readlines()
                for linea in lineas[-5:]:
                    print(f"   [LOG] {linea.strip()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    probar_bot()
