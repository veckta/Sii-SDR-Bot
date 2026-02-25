import requests
import json
import time

# URL de nuestro backend de FastAPI corriendo localmente
WEBHOOK_URL = "http://localhost:8000/webhook"

def enviar_mensaje_simulado(numero_origen="5491112345678", texto="Hola, necesito ayuda."):
    """Envía un payload simulando un webhook de mensaje de texto de WhatsApp"""
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
                                "display_phone_number": "123456789",
                                "phone_number_id": "987654321"
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "Usuario Prueba"},
                                    "wa_id": numero_origen
                                }
                            ],
                            "messages": [
                                {
                                    "from": numero_origen,
                                    "id": "wamid.HBgL...",
                                    "timestamp": str(int(time.time())),
                                    "text": {"body": texto},
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

    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        print(f"[Simulador] Enviado -> {texto}")
        print(f"[Simulador] Respuesta servidor: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("[Simulador] Error: El servidor FastAPI no está corriendo. Ejecuta 'uvicorn app:app --reload' primero.")

if __name__ == "__main__":
    print("=== SIMULADOR DE CHATS DE WHATSAPP ===")
    print("Escribe mensajes para ver cómo responde el webhook (escribe 'salir' para terminar).")
    
    while True:
        msg = input("\nMensaje Simulador: ")
        if msg.lower() == 'salir':
            break
        enviar_mensaje_simulado(texto=msg)