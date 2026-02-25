def enviar_resumen_diagnostico(numero_cliente: str, historial_chat: list):
    """
    Simula el envío de un resumen de diagnóstico al CRM o correo de la empresa
    una vez que el bot cognitivo logra que el usuario elija A, B o C.
    """
    print("==================================================")
    print("ENVIANDO REPORTE A CRM / CORREO DE S.I.I.")
    print("==================================================")
    print(f"Número de Cliente: {numero_cliente}")
    print("Historial de Diagnóstico:")
    
    # Ignoramos el system prompt
    for mensaje in historial_chat:
        if mensaje["role"] != "system":
            rol = "Cliente" if mensaje["role"] == "user" else "Bot SII"
            print(f" - {rol}: {mensaje['content']}")
            
    print("==================================================")
    print("REPORTE ENVIADO EXITOSAMENTE.")
    print("==================================================")
    
    # Aquí iría la lógica real usando la API de SendGrid, Mailgun 
    # o peticiones POST al endpoint de un CRM como HubSpot, Zoho, etc.
    return True