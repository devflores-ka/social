from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import mysql.connector
from mysql.connector import Error
from typing import Optional
from datetime import datetime
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

    # Validar la fecha de nacimiento con @field_validator
    @field_validator('dob')
    def validate_dob(cls, v):
        try:
            # Intentamos parsear la fecha en el formato 'yyyy-MM-dd'
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError("La fecha de nacimiento debe estar en formato 'yyyy-MM-dd'")
        return v

# Conexión a MariaDB usando las variables de entorno
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    if conn.is_connected():
        print("Conexión exitosa a la base de datos")
    return conn

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/api/usuarios/")
async def register_user(user: User):
    # Verificación de edad
    try:
        # Convertimos la fecha de nacimiento en un objeto datetime
        dob = datetime.strptime(user.dob, '%Y-%m-%d')
        age = user.age
        current_date = datetime.now()
        # Calculamos la edad
        calculated_age = current_date.year - dob.year
        if current_date.month < dob.month or (current_date.month == dob.month and current_date.day < dob.day):
            calculated_age -= 1
        
        # Verificamos si la edad es mayor o igual a 18
        if calculated_age < 18:
            raise HTTPException(status_code=400, detail="Debe tener al menos 18 años")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    print(user)  # Esto te permitirá ver si los datos llegan correctamente
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
