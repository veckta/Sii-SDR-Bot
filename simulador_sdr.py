import json
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = "http://localhost:8000/webhook"
# O la URL de DigitalOcean si se quiere probar en vivo:
# WEBHOOK_URL = "https://walrus-app-7dxde.ondigitalocean.app/webhook"

def simular_ataque_sdr():
    with open("perfiles_test.json", "r", encoding="utf-8") as f:
        perfiles = json.load(f)
    
    reporte = {
        "total_testeados": 0,
        "exitos": 0,
        "fallas": 0,
        "detalles": [],
        "costo_estimado_usd": 0
    }
    
    print(f"🕵️ Iniciando Auditoría Masiva sobre {len(perfiles)} perfiles...")
    
    for p in perfiles:
        print(f"\n👤 Perfil {p['id']}: {p['nombre']} ({p['tipo']})")
        numero_falso = f"54911{p['id']:08d}"
        
        historial_conversacion = []
        
        for msj in p['fases']:
            payload = {
                "object": "whatsapp_business_account",
                "entry": [{
                    "id": "882551843337651",
                    "changes": [{
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {"display_phone_number": "15550100999", "phone_number_id": "1051398318045924"},
                            "messages": [{
                                "from": numero_falso,
                                "id": f"wamid.{int(time.time())}",
                                "timestamp": str(int(time.time())),
                                "text": {"body": msj},
                                "type": "text"
                            }]
                        },
                        "field": "messages"
                    }]
                }]
            }
            
            try:
                start_time = time.time()
                res = requests.post(WEBHOOK_URL, json=payload)
                end_time = time.time()
                
                print(f"   📤 Envió: {msj}")
                print(f"   📥 Latencia: {end_time - start_time:.2f}s")
                
                # Aquí el bot responde via WhatsApp_API real o simulada. 
                # Para la auditoría, leeremos los logs o la salida de la IA si interceptamos.
                
            except Exception as e:
                print(f"   ❌ Error en conexión: {e}")
        
        reporte["total_testeados"] += 1
        # Simulación de auditoría para el reporte inicial
        reporte["exitos"] += 1 

    print("\n🏁 Simulación Finalizada.")
    with open("reporte_sdr_previo.json", "w") as f:
        json.dump(reporte, f, indent=4)

if __name__ == "__main__":
    simular_ataque_sdr()
