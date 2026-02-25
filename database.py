import json
import os
from datetime import datetime

DB_FILE = "sesiones_db.json"

def cargar_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def guardar_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def obtener_mensajes(numero):
    db = cargar_db()
    return db.get(numero, {}).get("historial", [])

def guardar_mensaje(numero, rol, contenido):
    db = cargar_db()
    if numero not in db:
        db[numero] = {"historial": [], "estado": "inicio", "ultima_actividad": ""}
    
    db[numero]["historial"].append({
        "role": rol,
        "content": contenido,
        "timestamp": datetime.now().isoformat()
    })
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
