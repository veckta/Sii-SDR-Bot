import uvicorn
import os

if __name__ == "__main__":
    # DigitalOcean inyecta el puerto en la variable de entorno 'PORT'
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
