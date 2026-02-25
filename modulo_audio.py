import os
from openai import OpenAI

# Inicializamos el cliente de OpenAI (agregamos llave dummy para evasión de crash en nube)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "dummy_key_para_evitar_crash"))

def transcribir_audio_whisper(ruta_archivo_audio: str) -> str:
    """
    Toma la ruta de un archivo de audio (ej: .ogg de WhatsApp, .mp3, .wav) 
    y utiliza el modelo Whisper-1 de OpenAI para devolver el texto transcrito.
    """
    try:
        if not os.path.exists(ruta_archivo_audio):
            return "Error: El archivo de audio no existe."

        print(f"[{ruta_archivo_audio}] Enviando a Whisper para transcripción...")
        with open(ruta_archivo_audio, "rb") as audio_file:
            transcripcion = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="text"
            )
        print("Transcripción completada con éxito.")
        return transcripcion
        
    except Exception as e:
        print(f"Error procesando el audio con Whisper: {e}")
        return ""

def generar_audio_base(texto: str, nombre_archivo_salida: str = "respuesta.mp3") -> str:
    """
    Toma un string de texto y utiliza Google TTS (gTTS) para 
    generar un archivo de audio hablado en español.
    Retorna la ruta del archivo generado.
    """
    try:
        from gtts import gTTS
        print(f"Sintetizando voz para el texto: '{texto}'...")
        tts = gTTS(text=texto, lang='es', tld='com.ar') # Voz en español (Acento sugerido Argentina)
        tts.save(nombre_archivo_salida)
        print(f"Audio generado y guardado en: {nombre_archivo_salida}")
        return nombre_archivo_salida
    except ImportError:
        print("Error: Falta instalar la librería gTTS. Ejecuta: pip install gTTS")
        return ""
    except Exception as e:
        print(f"Error generando TTS: {e}")
        return ""

if __name__ == "__main__":
    print("=== PRUEBA DE MÓDULO STT Y TTS ===")
    print("Para probar STT, coloca un archivo llamado 'prueba.ogg' en esta carpeta.")
    
    if os.environ.get("OPENAI_API_KEY"):
        # Crea un archivo dummy pidiendo al usuario que lo reemplace
        archivo_prueba = "prueba.ogg"
        if os.path.exists(archivo_prueba):
            texto = transcribir_audio_whisper(archivo_prueba)
            print(f"TEXTO OBTENIDO:\n{texto}")
        else:
            print("No se encontró 'prueba.ogg'. Crea un audio o copia uno para probar Whisper.")
            
        print("\n--- Probando TTS ---")
        texto_prueba = "Hola, bienvenido a Soluciones Inteligentes. ¿En qué te puedo ayudar hoy?"
        generar_audio_base(texto_prueba, "prueba_salida.mp3")
        
    else:
        print("Falta configurar OPENAI_API_KEY.")