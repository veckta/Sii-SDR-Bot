import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not url or not key:
    print("❌ ERROR: Faltan credenciales en el .env")
    exit(1)

# Endpoint de REST de Supabase
rest_url = f"{url.rstrip('/')}/rest/v1/historial_chats"

headers = {
    "apikey": key,
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation" # Pedimos que devuelva el objeto para confirmar
}

test_data = {
    "whatsapp_id": "TEST_SISTEMA",
    "role": "system",
    "mensaje": "Prueba de diagnóstico de conexión",
    "clasificacion_sdr": "TEST"
}

print(f"🚀 Intentando insertar en: {rest_url}")

try:
    with httpx.Client() as client:
        res = client.post(rest_url, json=test_data, headers=headers)
        
        print(f"Status Code: {res.status_code}")
        if res.status_code in [200, 201]:
            print("✅ ¡ÉXITO! El mensaje de prueba se insertó correctamente.")
            print("Payload devuelto:", json.dumps(res.json(), indent=2))
        else:
            print("❌ FALLA EN SUPABASE")
            print("Respuesta del servidor:", res.text)
            
            if res.status_code == 404:
                print("\n👉 ERROR 404: Esto suele significar que la TABLA 'historial_chats' no existe.")
            elif res.status_code == 401 or res.status_code == 403:
                print("\n👉 ERROR DE PERMISOS: La KEY de Supabase podría estar mal o falta RLS.")
            elif res.status_code == 400:
                print("\n👉 ERROR DE ESTRUCTURA: Probablemente un nombre de columna no coincide.")

except Exception as e:
    print(f"❌ ERROR DE RED/PYTHON: {e}")
