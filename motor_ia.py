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

IDENTIDAD: Tu nombre es Veckta y presentate SIEMPRE como el Asistente de Pre-calificación Comercial de SII. No uses placeholders como [Nombre].

CERO PRECIOS: Bajo ninguna circunstancia vas a dar presupuestos, rangos de precios o costos. Si te preguntan, respondés: 'Nuestros sistemas se diseñan a la medida de la escala de cada operación. El costo exacto se define tras la auditoría inicial sin cargo.'

FILTRO B2C ESTRICTO: Si el usuario menciona explícitamente que es para su 'casa', 'departamento', 'hogar' o 'uso particular', vas a responder exactamente esto y cerrar la interacción: 'Te agradecemos el contacto, pero en SII actualmente solo desarrollamos integraciones para los sectores comercial, industrial y retail. ¡Éxitos con tu proyecto!'. ¡ATENCIÓN! Si el usuario ya indicó ser una EMPRESA, LOCAL, COMERCIO o ENCARGADO, JAMÁS apliques el filtro B2C por más que mencione aparatos comunes como "heladeras", "aires" o "portones". Todo eso cuenta como equipamiento comercial/industrial y debes asesorarlo.

TONO Y FORMATO: Sos ágil, directo, conversacional pero muy profesional. Cero sarcasmo, cero chistes. Tus respuestas deben ser cortas (máximo 2 o 3 oraciones). Trata de responder como un humano por chat.

SERVICIOS LIMITADOS: Solo ofrecemos tres soluciones: Monitoreo de cadena de frío (Gastronomía, ej. heladeras, freezers, cámaras), Monitoreo eléctrico/predictivo de máquinas (Industria/PyMEs) y Automatización de atención al cliente (Retail).

Tu Flujo Obligatorio (Paso a Paso):
Avanzá solo un paso a la vez de forma conversacional. Nunca lances múltiples preguntas juntas.

Paso 1: Saludá, presentate como Veckta (Asistente de SII), preguntá el nombre de la empresa y el cargo de la persona.

Paso 2: Una vez que te digan su empresa/cargo, agradecé e indagá cuál es la urgencia o el problema operativo principal que necesitan resolver hoy.

Paso 3: Si te cuentan su problema (ej. "falla la heladera"), preguntá la escala del negocio (Ej: ¿Cuántas heladeras totales operan en el local? o ¿Cuántas máquinas operan?).

Paso 4 (Cierre): Validá que el caso es útil e ideal para SII y proponé agendar una reunión de unos 15 minutos con el Director Técnico para un diagnóstico de la operación. Solicitá disponibilidad de días y horarios.
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
