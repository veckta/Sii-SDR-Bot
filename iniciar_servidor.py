import subprocess
import sys
import time
import urllib.request

print("[servidor] Lanzando uvicorn en background...")
proceso = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app:app",
     "--host", "0.0.0.0", "--port", "8000", "--env-file", ".env"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print(f"[servidor] PID = {proceso.pid}. Esperando 4 segundos...")
time.sleep(4)

try:
    with urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5) as r:
        print(f"[servidor] OK - Respuesta: {r.read(100)}")
except Exception as e:
    print(f"[servidor] ERROR al verificar: {e}")

print("[servidor] Script finalizado. Uvicorn sigue corriendo en background.")
