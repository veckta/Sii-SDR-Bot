import requests

url = "https://walrus-app-7dxde.ondigitalocean.app/logs"
try:
    response = requests.get(url)
    with open("do_logs.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Logs guardados en do_logs.html")
except Exception as e:
    print("ERROR:", e)
