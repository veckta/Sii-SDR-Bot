import os
from dotenv import load_dotenv
import requests

load_dotenv()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
# WABA Oficial de SII
WABA_ID = "1072729585054018"
GRAPH_API_VERSION = "v18.0"

def suscribir_waba():
    print(f"🚀 Iniciando suscripción forzada del WABA: {WABA_ID}")
    
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    url_get = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{WABA_ID}/subscribed_apps"
    print(f"\n[1] Consultando suscripciones actuales...")
    res_get = requests.get(url_get, headers=headers)
    print(f"Estado: {res_get.status_code}")
    print(f"Respuesta: {res_get.text}")
    
    print(f"\n[2] Forzando POST a subscribed_apps...")
    res_post = requests.post(url_get, headers=headers)
    print(f"Estado: {res_post.status_code}")
    print(f"Respuesta: {res_post.text}")

if __name__ == "__main__":
    if not WHATSAPP_TOKEN:
        print("❌ ERROR: No se encontró WHATSAPP_TOKEN en .env")
    else:
        suscribir_waba()
