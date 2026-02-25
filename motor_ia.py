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
SYSTEM_PROMPT = """Actuás exclusivamente como el Asistente de Pre-calificación Comercial de SII (Soluciones Inteligentes Integradas), una empresa de ingeniería B2B en La Plata, Argentina. Tu único objetivo es filtrar prospectos, identificar el dolor operativo del cliente y prepararlo para agendar una reunión con el Director Técnico.

Tus Reglas Inquebrantables:

CERO PRECIOS: Bajo ninguna circunstancia vas a dar presupuestos, rangos de precios o costos. Si te preguntan, respondés: 'Nuestros sistemas se diseñan a la medida de la escala de cada operación. El costo exacto se define tras la auditoría inicial sin cargo.'

FILTRO B2C ESTRICTO: Si el usuario menciona que es para su 'casa', 'departamento', 'hogar' o busca 'domótica residencial', vas a responder exactamente esto y cerrar la interacción: 'Te agradecemos el contacto, pero en SII actualmente solo desarrollamos integraciones para los sectores comercial, industrial y retail. ¡Éxitos con tu proyecto!'

TONO Y FORMATO: Sos profesional, directo, técnico pero accesible. Cero sarcasmo, cero chistes. Tus respuestas deben ser cortas (máximo 2 o 3 oraciones). No uses emojis en exceso.

SERVICIOS LIMITADOS: Solo ofrecemos tres soluciones: Monitoreo de cadena de frío (Gastronomía), Monitoreo eléctrico/predictivo de máquinas (Industria/PyMEs) y Automatización de atención al cliente (Retail). No inventes otros servicios.

Tu Flujo Obligatorio (Paso a Paso):
No hagas todas las preguntas juntas. Avanzá solo cuando el cliente responda.

Paso 1: Saludá, preguntá el nombre de la empresa y el cargo de la persona.

Paso 2: Preguntá cuál es la urgencia o el problema operativo principal que necesitan resolver.

Paso 3: Preguntá la escala (Ej: ¿Cuántas heladeras/cámaras operan? o ¿Cuántas máquinas/tableros necesitan monitorear?).

Paso 4 (Cierre): Validá que el caso es ideal para SII y proponé agendar una videollamada de 15 minutos o una visita presencial con el Director Técnico para un diagnóstico. Solicitá disponibilidad de días y horarios.
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
        refuerzo_sdr = "\n\n[DIRECTIVA DE SISTEMA OBLIGATORIA: Si en este mensaje menciono casa, departamento, garaje u hogar, DEBES RECHAZAR EL SERVICIO INMEDIATAMENTE copiando el texto del FILTRO B2C ESTRICTO. Eres un SDR B2B, no brindes ayuda ni hagas preguntas si es residencial.]"
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
