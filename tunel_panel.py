import subprocess
import time
import os
import sys

def lanzar_todo():
    print("🚀 Iniciando Ecosistema de Auditoría SII...")
    
    # 1. Iniciar Streamlit en segundo plano
    print("📊 Levantando Dashboard Local...")
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "panel.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    time.sleep(5) # Esperar a que Streamlit caliente
    
    # 2. Iniciar Túnel de Cloudflare
    print("🌐 Abriendo Túnel Seguro a la Nube...")
    cloudflared_path = os.path.join(os.getcwd(), "cloudflared.exe")
    
    if not os.path.exists(cloudflared_path):
        print("❌ Error: No se encuentra cloudflared.exe en la carpeta actual.")
        streamlit_proc.terminate()
        return

    # Usamos try/except para manejar la interrupción del usuario
    try:
        # Lanzamos el túnel apuntando al puerto de streamlit
        subprocess.run([cloudflared_path, "tunnel", "--url", "http://localhost:8501"])
    except KeyboardInterrupt:
        print("\n🛑 Cerrando servicios...")
    finally:
        streamlit_proc.terminate()
        print("✅ Todo cerrado correctamente.")

if __name__ == "__main__":
    lanzar_todo()
