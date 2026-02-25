import subprocess
import threading
import re
import os

def iniciar_tunel():
    print("Iniciando túnel Serveo (IPv4 forzado)...")
    proceso = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no",
         "-o", "ServerAliveInterval=30",
         "-R", "80:127.0.0.1:8000", "serveo.net"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    url_encontrada = None
    for linea in proceso.stdout:
        print(f"[Serveo] {linea.strip()}")
        if "https://" in linea and not url_encontrada:
            match = re.search(r'(https://[^\s]+)', linea)
            if match:
                url_encontrada = match.group(1)
                webhook_url = url_encontrada + "/webhook"
                with open("tunel_url.txt", "w") as f:
                    f.write(webhook_url)
                print(f"\n{'='*60}")
                print(f"WEBHOOK URL: {webhook_url}")
                print(f"{'='*60}\n")

    proceso.wait()
    print("Túnel Serveo cerrado.")

if __name__ == "__main__":
    iniciar_tunel()
