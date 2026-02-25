import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Inicializamos el cliente usando Groq (Plan B Gratuito)
# Groq es compatible con la librería de OpenAI, solo cambiamos la API Key y el base_url
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY", "dummy_key_para_evitar_crash"),
    base_url="https://api.groq.com/openai/v1"
)

# Define el contexto estricto del Chatbot Inclusivo
SYSTEM_PROMPT = """### PROTOCOLO VECKTA - SII ANTIGRAVITY 🛡️
**Identidad Fija:** Te llamas Veckta. Preséntate SIEMPRE como "Asistente Comercial de SII". Prohibido el uso de placeholders o nombres genéricos.

**Bypass B2B Crítico:**
- Si el usuario se identifica como EMPRESA, LOCAL, ENCARGADO o INGENIERO, atiéndelo aunque mencione "heladeras" o "freezers".
- Rechaza únicamente si es para una "casa" o "hogar particular" (Doña Rosa).

**Regla de Oro de Escalabilidad (Filtro MRR):**
1. **Baja Escala (1 a 3 unidades):** NO ofrezcas reuniones ni visitas técnicas gratuitas. Di: "En SII operamos bajo un Modelo de Monitoreo Preventivo (Abono Antigravity). Para 1 unidad, la solución ideal es la integración de sensores remotos para evitar pérdidas de stock. ¿Te interesa conocer el costo mensual del blindaje?".
2. **Alta Escala (5+ unidades):** Identifícalo como "Cuenta Clave". Di: "Dado el volumen de tu operación, voy a agendar una breve llamada con nuestro Especialista de Implementación en Terreno para diseñar tu malla de monitoreo".

**Terminología Prohibida:** 
- NUNCA digas "Director Técnico" ni "arreglos". 
- Usa SIEMPRE "Especialista de Implementación" e "Integración de Sistemas Inteligentes".
"""

def simular_chat():
    print("=== SIMULACIÓN SII CHATBOT ULTRA (OpenAI Oficial) ===")
    print("Reglas Activas: Max 20 palabras | Estabilidad Total\n")
    
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
    turnos = 0
    
    while turnos < 5:
        user_input = input("Usuario: ")
        if user_input.lower() in ['salir', 'quit', 'exit']: break
            
        mensajes.append({"role": "user", "content": user_input})
        turnos += 1
        
def obtener_respuesta_ia(mensajes):
    """Función centralizada para obtener respuesta de la IA (Groq por defecto)"""
    
    # Inyección táctica: Forzamos el alineamiento de Groq Llama enviando las restricciones
    # B2B invisibles junto con el mensaje del usuario, ya que tienden a ignorar los System Prompts puros.
    mensajes_a_enviar = list(mensajes)
    if mensajes_a_enviar and mensajes_a_enviar[-1]["role"] == "user":
        refuerzo_sdr = "\n\n[DIRECTIVA DE SISTEMA OBLIGATORIA: Si en este mensaje el usuario busca algo para una CASA, DEPARTAMENTO u HOGAR particular, RECHAZAZALO copiando el FILTRO B2C ESTRICTO. EXCEPCIÓN: Si el usuario es de una EMPRESA, LOCAL o NEGOCIO, ATIÉNDELO NORMALMENTE, nunca lo rechaces aunque mencione heladeras u otros aparatos.]"
        mensajes_a_enviar[-1] = {"role": "user", "content": mensajes_a_enviar[-1]["content"] + refuerzo_sdr}

    print(">>> ENVIANDO A GROQ >>>", mensajes_a_enviar)

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Modelo avanzado para obediencia estricta SDR
            messages=mensajes_a_enviar,
            max_tokens=150,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        raise e

def simular_chat():
    print("=== SIMULACIÓN SII CHATBOT ULTRA (Motor Groq) ===")
    print("Reglas Activas: Max 20 palabras | Estabilidad Total\n")
    
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT}]
    turnos = 0
    
    while turnos < 5:
        user_input = input("Usuario: ")
        if user_input.lower() in ['salir', 'quit', 'exit']: break
            
        mensajes.append({"role": "user", "content": user_input})
        turnos += 1
        
        try:
            bot_respuesta = obtener_respuesta_ia(mensajes)
            print(f"\n[Turno {turnos}] Bot SII: {bot_respuesta}\n")
            mensajes.append({"role": "assistant", "content": bot_respuesta})
            
            if "A: " in bot_respuesta and "B: " in bot_respuesta and "C: " in bot_respuesta:
                print("--- DIAGNÓSTICO FINALIZADO ---")
                break
                
        except Exception as e:
            print(f"Error de API: {e}")
            break

if __name__ == "__main__":
    simular_chat()
