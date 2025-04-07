from fastapi import FastAPI
from .api.endpoints import router  # Importa el router desde endpoints.py
from .database.connection import check_connection

app = FastAPI(title="User Authentication API")

@app.on_event("startup")
async def startup_db_client():
    # Verificar conexión a MongoDB al iniciar la aplicación
    await check_connection()

# Incluir el router sin prefijo
app.include_router(router)  
for route in app.routes:
    print(f"Path: {route.path}, Method: {route.methods}")
    