import subprocess
import os
import sys
import time
import re
import signal

# Configuración
PORT = 8000
APP_MODULE = "app:app"
LOG_FILE = "app_console.log"
ENV_FILE = ".env"
TUNEL_FILE = "tunel_url.txt"

def kill_process_by_port(port):
    """Limpia el puerto si está ocupado (Windows)"""
    try:
        output = subprocess.check_output(f"netstat -ano | findstr :{port}", shell=True).decode()
        for line in output.strip().split("\n"):
            if "LISTENING" in line:
                pid = line.strip().split()[-1]
                print(f"[Manager] Limpiando puerto {port} (PID: {pid})...")
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
    except:
        pass

def kill_serveo_ssh():
    """Mata procesos ssh que podrían ser túneles viejos"""
    try:
        subprocess.run("taskkill /F /IM ssh.exe", shell=True, capture_output=True)
        print("[Manager] Procesos SSH cerrados.")
    except:
        pass

def iniciar():
    print("\n" + "="*40)
    print("🚀 SII CHATBOT PRO - ORQUESTADOR")
    print("="*40 + "\n")

    # 1. Limpieza
    kill_process_by_port(PORT)
    kill_serveo_ssh()

    # 2. Iniciar Servidor
    print(f"[Manager] Iniciando servidor en puerto {PORT}...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", APP_MODULE, "--host", "127.0.0.1", "--port", str(PORT), "--env-file", ENV_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)

    # 3. Iniciar Túnel
    print("[Manager] Iniciando túnel Serveo...")
    ssh_proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-R", f"80:127.0.0.1:{PORT}", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    url_encontrada = None
    print("[Manager] Esperando URL del túnel...")
    
    # Timeout de 30 segundos para encontrar la URL
    start_time = time.time()
    if ssh_proc.stdout:
        while time.time() - start_time < 30:
            linea = ssh_proc.stdout.readline()
            if not linea: break
            
            linea_clean = linea.strip()
            print(f"[Serveo] {linea_clean}")
            if "https://" in linea_clean:
                # Regex robusto para capturar solo la URL
                match = re.search(r'(https://[a-zA-Z0-9\-\.]+serveousercontent\.com)', linea_clean)
                if match:
                    url_encontrada = match.group(1)
                    webhook_url = url_encontrada + "/webhook"
                    with open(TUNEL_FILE, "w") as f:
                        f.write(webhook_url)
                    
                    print("\n" + "!"*40)
                    print(f"✅ SISTEMA ULTRA+ ONLINE")
                    print(f"URL: {webhook_url}")
                    print("!"*40 + "\n")
                    break
    
    if not url_encontrada:
        print("\n❌ ERROR: No se pudo obtener la URL del túnel.")
        print("Revisá tu conexión a internet o si Serveo está saturado.")
    
    print("[Manager] El sistema está corriendo en segundo plano.")
    print("Podés cerrar este script, pero el servidor y el túnel seguirán activos.")

if __name__ == "__main__":
    iniciar()
