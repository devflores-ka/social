from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from mysql.connector import Error
from typing import Optional
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Definir el modelo de los datos
class User(BaseModel):
    uid: str
    full_name: str
    dob: str
    gender: str
    age: int
    role: str
    profile_photo_url: Optional[str] = None  # Campo opcional para la URL de S3
    verification_photo_url: Optional[str] = None  # URL de la foto para verificación en S3

# Conexión a MariaDB usando las variables de entorno
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

@app.post("/api/usuarios/")
async def register_user(user: User):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (uid, full_name, dob, gender, age, role, profile_photo_url, verification_photo_url) VALUES (%s, %s, %s, %s, %s, %s, NULL, NULL)",
            (user.uid, user.full_name, user.dob, user.gender, user.age, user.role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Usuario registrado exitosamente"}
    except Error as e:
        return {"error": f"Error al registrar el usuario: {str(e)}"}
