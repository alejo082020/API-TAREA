from fastapi import APIRouter, HTTPException, status
from ..database.connection import collection
from ..schemas.user import UserCreate, User, UserLogin
from ..auth.utils import verify_password, get_password_hash
from datetime import datetime, timedelta
from jose import JWTError, jwt

router = APIRouter()
router = APIRouter(prefix="/api")
SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
@router.post("/users/register", response_model=User, tags=["auth"])
async def register(user: UserCreate):
    # Verificar si el usuario ya existe
    if await collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    await collection.insert_one(new_user)
    return {"username": user.username, "email": user.email}

@router.post("/users/login", tags=["auth"])
async def login(user: UserLogin):
    try:
        # Buscar usuario
        db_user = await collection.find_one({"username": user.username})
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        # Verificar contraseña
        if not verify_password(user.password, db_user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        # Generar token de acceso
        access_token = create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
@router.delete("/users/{username}")
async def delete_user(username: str):
    # Eliminar usuario
    result = await collection.delete_one({"username": username})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}
