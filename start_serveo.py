import subprocess
import time
import re

print("Iniciando túnel Serveo en 127.0.0.1:8000 y guardando URL...")
proceso = subprocess.Popen(
    ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:127.0.0.1:8000", "serveo.net"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

url_encontrada = ""
for i in range(15):
    linea = proceso.stdout.readline()
    if linea:
        print(linea.strip())
        if "https://" in linea:
            match = re.search(r'(https://[^\s]+)', linea)
            if match:
                url_encontrada = match.group(1)
                with open("serveo_url.txt", "w") as f:
                    f.write(url_encontrada)
                break
    time.sleep(0.5)

print(f"URL Guardada: {url_encontrada}")
print("El túnel está ACTIVO. Manteniendo proceso abierto...")
while True:
    time.sleep(10)
