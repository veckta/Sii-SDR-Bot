import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def registrar_mensaje(whatsapp_id, role, mensaje, clasificacion=None):
    """
    Inserta un mensaje en la tabla historial_chats de Supabase usando la API REST.
    Diseñado para ser invocado vía BackgroundTasks de FastAPI.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        return

    # Construimos la URL de la tabla (PostgREST API)
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/historial_chats"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    data = {
        "whatsapp_id": str(whatsapp_id),
        "role": role,
        "mensaje": mensaje,
        "clasificacion_sdr": clasificacion
    }
    
    try:
        # Usamos un timeout corto para no quedar colgados
        with httpx.Client(timeout=5.0) as client:
            res = client.post(url, json=data, headers=headers)
            res.raise_for_status()
            return res
    except Exception as e:
        # En producción redireccionamos a logs internos para no romper el flujo
        print(f"[SUPABASE REST ERROR] {e}")
        return None
