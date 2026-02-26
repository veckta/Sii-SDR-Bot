import motor_ia

print("=== INICIANDO PRUEBA DE FILTRO MRR (Capa 4) ===")

mensajes_simulados = [
    {"role": "system", "content": motor_ia.SYSTEM_PROMPT},
    {"role": "user", "content": "Hola, buenas intenciones"},
    {"role": "assistant", "content": "Hola, soy Veckta, el Asistente Comercial de SII. Un placer saludarte. ¿En qué puedo ayudarte hoy con la optimización inteligente de tu negocio o industria?"},
    {"role": "user", "content": "Soy Ariel, encargado de una fábrica de pastas acá en La Plata. Se nos rompió una heladera comercial de la cámara y estamos perdiendo mercadería. ¿Hacen arreglos?"},
    {"role": "assistant", "content": "Entendido, Ariel. Al ser una fábrica de pastas, comprendo la urgencia por la cadena de frío. ¿Cuántos equipos de frío (heladeras o freezers) necesitás monitorear y contás con Wi-Fi en la planta de producción?"},
    {"role": "user", "content": "Tenemos solo 1 cámara con problemas."} 
]

print("\n--- Contexto Inyectado ---")
print("El cliente acaba de responder que solo tiene 1 cámara.")
print("Verificando cómo reacciona Veckta (Debería ignorar la reunión y ofrecer el Abono Preventivo)...")

respuesta = motor_ia.obtener_respuesta_ia(mensajes_simulados)
print("\n[VECKTA RESPONDE]:\n", respuesta)
print("\n================================================")
