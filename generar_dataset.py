import json
import random
import os

locaciones = ["Los Hornos", "Gonnet", "City Bell", "Ensenada", "Berisso", "Tolosa", "Villa Elvira", "San Lorenzo", "Calle 12", "Centro"]
negocios = ["Frigorífico", "Carnicería", "Supermercado", "Kiosco", "Autoservicio", "Fiambrería", "Heladería", "Depósito"]
problemas = ["perdí frío", "se cortó la luz", "quiero monitorear", "busco seguridad térmica", "me avisaron que falló"]

perfiles = []

# Cargar base si existe
if os.path.exists("perfiles_test.json"):
    try:
        with open("perfiles_test.json", "r", encoding="utf-8") as f:
            perfiles = json.load(f)
    except:
        perfiles = []

current_id = len(perfiles) + 1

while len(perfiles) < 50:
    tipo_r = random.choice(["B2B_ALTA", "B2B_BAJA", "B2C", "AMBIGUO"])
    loc = random.choice(locaciones)
    neg = random.choice(negocios)
    
    if tipo_r == "B2B_ALTA":
        num_e = random.randint(5, 12)
        p = {
            "id": current_id,
            "tipo": tipo_r,
            "nombre": f"Lead {neg} {loc} ({num_e} equipos)",
            "fases": [
                f"Hola, hablo desde un {neg} en {loc}.",
                f"Tengo {num_e} equipos de frío que necesitan control.",
                "¿Tienen servicio para empresas grandes?"
            ],
            "objetivo_esperado": "DERIVAR_ESPECIALISTA"
        }
    elif tipo_r == "B2B_BAJA":
        num_e = random.randint(1, 3)
        p = {
            "id": current_id,
            "tipo": tipo_r,
            "nombre": f"Local {neg} {loc} ({num_e} equipos)",
            "fases": [
                f"Tengo un {neg} chico en {loc}.",
                f"Uso {num_e} heladeras nada más.",
                "Quiero saber el precio del sensor mensual."
            ],
            "objetivo_esperado": "OFRECER_ABONO"
        }
    elif tipo_r == "B2C":
        p = {
            "id": current_id,
            "tipo": tipo_r,
            "nombre": f"Particular en {loc}",
            "fases": [
                "Hola, ¿hacen alarmas para casas?",
                f"Es mi domicilio particular en {loc}.",
                "Necesito que me avise al cel si entran."
            ],
            "objetivo_esperado": "RECHAZAR_AMABLEMENTE"
        }
    else: # AMBIGUO
        p = {
            "id": current_id,
            "tipo": tipo_r,
            "nombre": f"Consulta Ambigua {loc}",
            "fases": [
                "Buenas, me pasaron este contacto.",
                "¿Qué servicios ofrecen?",
                "Tengo un negocio pequeño."
            ],
            "objetivo_esperado": "INDAGAR_DETALLES"
        }
    
    perfiles.append(p)
    current_id += 1

with open("perfiles_test.json", "w", encoding="utf-8") as f:
    json.dump(perfiles, f, indent=2, ensure_ascii=False)

print(f"✅ Dataset de {len(perfiles)} perfiles generado con éxito.")
