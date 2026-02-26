import sys
import os
import json
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from motor_ia import client, SYSTEM_PROMPT
from modulo_audio import transcribir_audio_whisper, generar_audio_base
from servicios_externos import enviar_resumen_diagnostico
import whatsapp_api
import database
import supabase_db
from fastapi import BackgroundTasks

# Configuración de logging estándar más robusta y compatible con la nube (DigitalOcean usa Linux /tmp/ para escrituras efímeras)
LOG_FILE = "/tmp/app_console.log" if "linux" in sys.platform else "app_console.log"
try:
    # Forzar UTF-8 en el handler de archivo
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    stream_handler = logging.StreamHandler(sys.stdout)
    # Algunos sistemas Windows necesitan que sys.stdout también se fuerce a utf-8 si no está configurado
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[file_handler, stream_handler]
    )
except Exception:
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger("SII-ULTRA-PRO")
logger.info("=== REINICIO DE SISTEMA SII ULTRA PRO ===")

app = FastAPI(title="SII Chatbot Pro - Backend")

VERIFY_TOKEN = "sii_token_secreto_2026"

@app.get("/")
def home():
    return {"status": "online", "system": "SII Chatbot Ultra"}

@app.get("/privacidad", response_class=HTMLResponse)
def privacidad():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Política de Privacidad - SII</title>
        <style>body { font-family: Arial; padding: 40px; line-height: 1.6; color: #333; max-width: 800px; margin: auto; }</style>
    </head>
    <body>
        <h1>Política de Privacidad</h1>
        <p><strong>Última actualización: Febrero 2026</strong></p>
        <p>Soluciones Inteligentes Integrales (SII) opera el Chatbot Inclusivo SII. Esta página le informa sobre nuestras políticas con respecto a la recopilación, el uso y la divulgación de datos personales cuando utiliza nuestro Servicio.</p>
        <h2>Recopilación y uso de la información</h2>
        <p>Recopilamos varios tipos de información con diversos fines para proporcionarle y mejorar nuestro Servicio. Su número de teléfono y el contenido de los mensajes de WhatsApp se utilizan exclusivamente para diagnosticar problemas y proporcionar asistencia técnica pre-aprobada mediante IA.</p>
        <h2>Retención de datos</h2>
        <p>Conservaremos sus Datos Personales solo durante el tiempo que sea necesario para los fines establecidos en esta Política de Privacidad.</p>
        <h2>Contacto</h2>
        <p>Si tiene alguna pregunta sobre esta Política de Privacidad, por favor contáctenos a través de nuestro WhatsApp oficial.</p>
    </body>
    </html>
    """
    return html

@app.get("/logs", response_class=HTMLResponse)
def ver_logs():
    """Dashboard Premium para monitorear el bot en tiempo real"""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            contenido = f.readlines()
            contenido = "".join(contenido[-100:])
    except Exception:
        contenido = "Esperando actividad..."
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>SII Command Center</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            :root {{ --bg: #0d0d0d; --green: #00ff41; --text: #e0e0e0; --accent: #007bff; }}
            body {{ background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; margin: 0; padding: 20px; }}
            .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
            .status {{ background: #1a1a1a; padding: 5px 15px; border-radius: 20px; color: var(--green); font-size: 12px; border: 1px solid var(--green); }}
            pre {{ background: #151515; padding: 15px; border-radius: 8px; font-size: 13px; line-height: 1.5; overflow-x: auto; border: 1px solid #333; color: #a5a5a5; white-space: pre-wrap; }}
            .highlight {{ color: var(--green); font-weight: bold; }}
            .out {{ color: #00ccff; }}
        </style>
        <script>
            setTimeout(() => location.reload(), 3000);
            window.onload = () => window.scrollTo(0, document.body.scrollHeight);
        </script>
    </head>
    <body>
        <div class="header">
            <h2 style="margin:0; color:white;">⚡ SII <span style="color:var(--accent)">ULTRA</span></h2>
            <div class="status">🟢 SISTEMA OPERATIVO</div>
        </div>
        <pre>{contenido.replace("[TEXTO ENTRANTE]", "<span class='highlight'>[TEXTO ENTRANTE]</span>")}</pre>
    </body>
    </html>
    """
    return html

@app.get("/webhook")
def verificar_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        logger.info("[WEBHOOK] Verificación exitosa de Meta.")
        return PlainTextResponse(content=challenge)
    raise HTTPException(status_code=403, detail="Error de verificación")

@app.post("/webhook")
async def recibir_mensaje_whatsapp(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.json()
        logger.info(f"[META RAW PAYLOAD] {json.dumps(body)}")
        if not body.get("object"): raise HTTPException(status_code=404)
        
        for entry in body.get("entry", []):
            for cambio in entry.get("changes", []):
                valor = cambio.get("value", {})
                metadata = valor.get("metadata", {})
                id_numero_receptor = metadata.get("phone_number_id")
                mensajes = valor.get("messages", [])
                
                for msj in mensajes:
                    numero_origen = msj.get("from")
                    tipo = msj.get("type")
                    texto_usuario = ""
                    
                    if tipo == "text":
                        texto_usuario = msj.get("text", {}).get("body", "")
                        logger.info(f"[TEXTO ENTRANTE] {numero_origen}: {texto_usuario}")
                    elif tipo == "audio":
                        audio_id = msj.get("audio", {}).get("id")
                        logger.info(f"[AUDIO ENTRANTE] {numero_origen}")
                        # logger.info(f"[TRANSCRIPCIÓN] {texto_usuario}") # El logger ya maneja utf-8, pero evitemos prints directos
                        pass
                    else: continue

                    respuesta = procesar_respuesta(numero_origen, texto_usuario, background_tasks)
                    
                    if tipo == "audio":
                        ruta_voz = generar_audio_base(respuesta)
                        whatsapp_api.enviar_mensaje_texto(numero_origen, respuesta, id_numero_receptor)
                        whatsapp_api.enviar_mensaje_audio(numero_origen, ruta_voz, id_numero_receptor)
                    else:
                        whatsapp_api.enviar_mensaje_texto(numero_origen, respuesta, id_numero_receptor)
                    
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"[ERROR WEBHOOK] {e}")
        return {"status": "error"}

def procesar_respuesta(numero, texto, background_tasks: BackgroundTasks = None):
    """Maneja el flujo delegando al motor_ia centralizado (Groq/OpenAI)"""
    import motor_ia
    
    # Registro Asíncrono en Supabase (User)
    if background_tasks:
        background_tasks.add_task(supabase_db.registrar_mensaje, numero, "user", texto)
    
    historial = database.obtener_mensajes(numero)
    
    # Asegurar que el Prompt del Sistema esté actualizado
    if not historial:
        database.guardar_mensaje(numero, "system", motor_ia.SYSTEM_PROMPT.strip())
    elif historial[0]["role"] == "system" and historial[0]["content"].strip() != motor_ia.SYSTEM_PROMPT.strip():
        # Si el prompt cambió, reseteamos la sesión para aplicar nuevas reglas comerciales
        logger.info(f"[SISTEMA] Cambio de Prompt detectado para {numero}. Reseteando sesión.")
        database.borrar_sesion(numero)
        database.guardar_mensaje(numero, "system", motor_ia.SYSTEM_PROMPT.strip())
    
    database.guardar_mensaje(numero, "user", texto)
    
    # Recargar historial para la IA
    mensajes_completos = database.obtener_mensajes(numero)
    mensajes_ia = [{"role": m["role"], "content": m["content"]} for m in mensajes_completos]

    try:
        # Llamamos al motor centralizado para obtener la respuesta
        bot_respuesta = motor_ia.obtener_respuesta_ia(mensajes_ia)
        
        database.guardar_mensaje(numero, "assistant", bot_respuesta)
        
        # Registro Asíncrono en Supabase (Assistant)
        if background_tasks:
             # Aquí podríamos extraer clasificación si se detecta cierre de venta
             clasif = None
             if "Abono Antigravity" in bot_respuesta: clasif = "Abono"
             elif "Especialista" in bot_respuesta: clasif = "Alta Escala"
             elif "exclusivos para comercios" in bot_respuesta: clasif = "Rechazo"
             
             background_tasks.add_task(supabase_db.registrar_mensaje, numero, "assistant", bot_respuesta, clasif)

        if "A: " in bot_respuesta and "B: " in bot_respuesta and "C: " in bot_respuesta:
            logger.info(f"[SISTEMA] Diagnóstico finalizado para {numero}")
            enviar_resumen_diagnostico(numero, mensajes_completos)
            database.borrar_sesion(numero)
            
        return bot_respuesta
    except Exception as e:
        logger.error(f"[ERROR IA] {e}")
        return "Disculpe, tuve un problema técnico. ¿Podemos retomar?"

