import os
import requests

# Tokens necesarios que el usuario sacará de Meta for Developers
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "")
GRAPH_API_VERSION = "v18.0"

def obtener_headers():
    return {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

def descargar_audio_whatsapp(audio_id: str) -> str:
    """Consigue la URL temporal del audio en Meta y lo descarga localmente."""
    if not WHATSAPP_TOKEN:
        print("[WhatsApp API] Faltan credenciales (WHATSAPP_TOKEN). Simulación de descarga.")
        return f"audio_simulado_{audio_id}.ogg"
        
    # 1. Obtener la URL del medio
    url_info = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{audio_id}"
    res_info = requests.get(url_info, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"})
    
    if res_info.status_code == 200:
        media_url = res_info.json().get("url")
        # 2. Descargar el archivo binario
        res_media = requests.get(media_url, headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"})
        if res_media.status_code == 200:
            ruta_local = f"descarga_{audio_id}.ogg"
            with open(ruta_local, "wb") as f:
                f.write(res_media.content)
            print(f"[WhatsApp API] Audio descargado desde Meta: {ruta_local}")
            return ruta_local
            
    print(f"[WhatsApp API] Error descargando audio {audio_id}: {res_info.text}")
    return ""

def enviar_mensaje_texto(numero_destino: str, texto: str, id_numero: str = None):
    """Envía un mensaje de texto simple de vuelta al cliente de WhatsApp."""
    id_final = id_numero or PHONE_NUMBER_ID
    if not WHATSAPP_TOKEN or not id_final:
        print(f"[Simulador Salida] A {numero_destino}: {texto}")
        return 200
        
    # Parche Argentina: Reemplazar 549 por 54...15 si es el número de Ariel
    if numero_destino == "5492216146709":
        numero_destino = "54221156146709"
        
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{id_final}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": numero_destino,
        "type": "text",
        "text": {"body": texto}
    }
    res = requests.post(url, headers=obtener_headers(), json=payload)
    return res.status_code

def enviar_mensaje_audio(numero_destino: str, ruta_audio_local: str, id_numero: str = None):
    """Sube el audio generado localmente a Meta y se lo envía al cliente de WhatsApp en un solo paso."""
    id_final = id_numero or PHONE_NUMBER_ID
    if not WHATSAPP_TOKEN or not id_final:
        print(f"[Simulador Salida] A {numero_destino}: (Audio MP3 = {ruta_audio_local})")
        return 200
        
    # Parche Argentina: Reemplazar 549 por 54...15 si es el número de Ariel
    if numero_destino == "5492216146709":
        numero_destino = "54221156146709"
        
    # 1. Subir el archivo multimedia (Audio) a Meta
    url_media = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{id_final}/media"
    headers_media = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
    
    try:
        with open(ruta_audio_local, "rb") as f:
            archivos = {
                "file": (ruta_audio_local, f, "audio/mpeg"),
                "type": (None, "audio"),
                "messaging_product": (None, "whatsapp")
            }
            res_media = requests.post(url_media, headers=headers_media, files=archivos)
            
        if res_media.status_code == 200:
            media_id = res_media.json().get("id")
            
            # 2. Enviar el ID del media como mensaje de voz
            url_msg = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{id_final}/messages"
            payload = {
                "messaging_product": "whatsapp",
                "to": numero_destino,
                "type": "audio",
                "audio": {"id": media_id}
            }
            res_msg = requests.post(url_msg, headers=obtener_headers(), json=payload)
            print(f"[WhatsApp API] Audio enviado a {numero_destino}")
            return res_msg.status_code
        else:
            print(f"[WhatsApp API] Error al subir media: {res_media.text}")
            return None
    except Exception as e:
        print(f"Error procesando envío de audio: {e}")
        return None