import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("WHATSAPP_TOKEN", "")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID", "")

print("=== Verificando estado del numero en Meta ===")

# 1. Ver info del PHONE_NUMBER_ID
url_phone = f"https://graph.facebook.com/v18.0/{PHONE_ID}"
r = requests.get(url_phone, params={"access_token": TOKEN, "fields": "display_phone_number,verified_name,quality_rating,id"})
print(f"\n[Phone ID Info] Status: {r.status_code}")
print(r.text[:400])

# 2. Ver si hay otra info del token
url_token_debug = "https://graph.facebook.com/debug_token"
r2 = requests.get(url_token_debug, params={
    "input_token": TOKEN,
    "access_token": TOKEN
})
print(f"\n[Token Debug] Status: {r2.status_code}")
print(r2.text[:400])
