import json
import os
from datetime import datetime

DB_FILE = "sesiones_db.json"
TTL_HOURS = 12
MAX_HISTORY = 10

def cargar_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)
            # Limpieza por TTL al cargar
            ahora = datetime.now()
            limpia = {}
            for num, data in db.items():
                ultima = datetime.fromisoformat(data.get("ultima_actividad", ahora.isoformat()))
                if (ahora - ultima).total_seconds() < (TTL_HOURS * 3600):
                    limpia[num] = data
            return limpia
    except:
        return {}

def guardar_db(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)


def obtener_mensajes(numero):
    db = cargar_db()
    return db.get(numero, {}).get("historial", [])

def guardar_mensaje(numero, rol, contenido):
    db = cargar_db()
    if numero not in db:
        db[numero] = {"historial": [], "estado": "inicio", "ultima_actividad": ""}
    
    # Agregar mensaje y limitar a los últimos MAX_HISTORY
    db[numero]["historial"].append({
        "role": rol,
        "content": contenido,
        "timestamp": datetime.now().isoformat()
    })
    
    if len(db[numero]["historial"]) > MAX_HISTORY:
        # Mantenemos el mensaje de sistema (índice 0) y los últimos N-1 mensajes
        system_msg = db[numero]["historial"][0] if db[numero]["historial"][0]["role"] == "system" else None
        new_hist = db[numero]["historial"][-MAX_HISTORY:]
        if system_msg and new_hist[0] != system_msg:
             new_hist = [system_msg] + new_hist[-(MAX_HISTORY-1):]
        db[numero]["historial"] = new_hist

    db[numero]["ultima_actividad"] = datetime.now().isoformat()
    guardar_db(db)

def borrar_sesion(numero):
    db = cargar_db()
    if numero in db:
        del db[numero]
        guardar_db(db)

def actualizar_estado(numero, estado):
    db = cargar_db()
    if numero in db:
        db[numero]["estado"] = estado
        guardar_db(db)

def obtener_estado(numero):
    db = cargar_db()
    return db.get(numero, {}).get("estado", "inicio")
