from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL de conexión a MongoDB Atlas
MONGO_URL = "mongodb+srv://ALEJANDRO:alejandro123@cluster0.ztfcx.mongodb.net/ALEJANDRO?retryWrites=true&w=majority"

try:
    # Intentar conectar a MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    # Usar la base de datos especificada en la URL
    db = client.ALEJANDRO
    collection = db.users
    
    # Verificar la conexión
    async def check_connection():
        try:
            await client.admin.command('ping')
            logger.info("✅ Conexión exitosa a MongoDB Atlas")
            return True
        except Exception as e:
            logger.error(f"❌ Error de conexión a MongoDB Atlas: {str(e)}")
            return False

except ConnectionFailure as e:
    logger.error(f"❌ No se pudo conectar a MongoDB Atlas: {str(e)}")
    raise
