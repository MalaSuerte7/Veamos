from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Permisos 
origins = [
    "*", #Todos los origenes 
]

# Database connection information
host_name = "database-1.crlz1rjtrz0e.us-east-1.rds.amazonaws.com"
port_number = "3306"  # El puerto para MySQL es normalmente 3306, no 8005
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "Train"

# Estructura para representar un entrenador usando Pydantic
class Trainer(BaseModel):
    id: int
    nombre: str
    dinero: int
# Estructura para representar un pokemons_de_entrenador usando Pydantic
#     cursor.execute(f"INSERT INTO pokemons_de_entrenador (nombre_entrenador, nombre_pokemon, id_pokemon, id_entrenador, sprite, nivel, HP, tipo) VALUES ({nombre_entrenador},

class pokemon_de_entrenador(BaseModel):
    id: int
    nombre_entrenador: str
    nombre_pokemon: str
    id_pokemon: int
    id_entrenador: int
    sprite: str
    nivel: int
    HP: int
    tipo: str

# objetos_de_entrenadoc
class objetos_de_entrenadoc(BaseModel):
    id: int
    nombre_entrenador: str
    id_entrenador: int
    nombre_objeto: str
    id_objeto: int
    cantidad: int

# Builds 

# Función para construir un objeto entrenador
def build_trainer_object(data):
    return {
        "id": data[0],
        "nombre": data[1],
        "dinero": data[2]
    }

# Función para construir un objeto pokemon de entrenador
def build_pokemon_de_entrenador_object(data):
    return {
        "id": data[0],
        "nombre_entrenador": data[1],
        "nombre_pokemon": data[2],
        "id_pokemon": data[3],
        "id_entrenador": data[4],
        "sprite": data[5],
        "nivel": data[6],
        "HP": data[7],
        "tipo": data[8]
    }

# Función para construir un objeto de entrenador
def build_objeto_de_entrenador_object(data):
    return {
        "id": data[0],
        "nombre_entrenador": data[1],
        "nombre_objeto": data[2],
        "id_entrenador": data[3],
        "id_objeto": data[4],
        "cantidad": data[5]
    }

# 
@app.get("/")
def read_root():
    return {"message": "Welcome to your Pokemon API!"}

# Get all trainers
@app.get("/trainers")
def get_trainers():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM entrenadores")
    result = cursor.fetchall()
    mydb.close()
    
    trainers = []
    for data in result:
        trainers.append(build_trainer_object(data))
    return {"trainers": trainers}


# Get a trainer by ID
@app.get("/trainers/{id}")
def get_trainer(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM entrenadores WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    
    trainer = build_trainer_object(result)
    return {"trainer": trainer}

# Add a new trainer
@app.post("/trainers")
def add_trainer(item: Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO entrenadores (nombre, dinero) VALUES (%s, %s)"
    val = (item.nombre, item.dinero)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Trainer added successfully"}

# Modify a trainer
@app.put("/trainers/{id}")
def update_trainer(id: int, item: Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE entrenadores SET dinero=%s WHERE id=%s"
    val = (item.dinero, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Trainer modified successfully"}

# Login
@app.post("/login")
def login(username: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM entrenadores WHERE nombre = '{username}'")
    result = cursor.fetchone()
    if result is None:
        cursor.execute(f"INSERT INTO entrenadores (nombre, dinero) VALUES ('{username}', 1000)")
        cursor.execute(f"SELECT * FROM entrenadores WHERE nombre = '{username}'")
        result = cursor.fetchone()
        mydb.commit()
    mydb.close()
    return {"trainer": result}

# Get Trainer pokemons
@app.get("/pokemons_de_entrenador/{id_entrenador}")
def get_pokemons_de_entrenador(id_entrenador: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM pokemons_de_entrenador WHERE id_entrenador = {id_entrenador}")
    result = cursor.fetchall()
    mydb.close()
    pokemons = []
    for data in result:
        pokemons.append(build_pokemon_de_entrenador_object(data))
    return {"pokemons": pokemons}


# Create a new pokemon for a trainer
@app.post("/crear_pokemon_de_entrenador")
def crear_pokemon_de_entrenador(nombre_entrenador: str, nombre_pokemon: str, id_pokemon: int, id_entrenador: int, sprite: str, nivel: int, HP: int, tipo: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"INSERT INTO pokemons_de_entrenador (nombre_entrenador, nombre_pokemon, id_pokemon, id_entrenador, sprite, nivel, HP, tipo) VALUES ('{nombre_entrenador}', '{nombre_pokemon}', {id_pokemon}, {id_entrenador}, '{sprite}', {nivel}, {HP}, '{tipo}')")
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon created successfully"}

# Show trainer inventory
@app.get("/objetos_de_entrenadoc/{id_entrenador}")
def get_objetos_de_entrenadoc(id_entrenador: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM objetos_de_entrenadoc WHERE id_entrenador = {id_entrenador}")
    result = cursor.fetchall()
    mydb.close()
    objetos = []
    for data in result:
        objetos.append(build_objeto_de_entrenador_object(data))
    return {"objetos": objetos}

# Create a new object for a trainer
@app.post("/crear_objeto_de_entrenador")
def crear_objeto_de_entrenador(nombre_entrenador: str, id_entrenador: int, nombre_objeto: str, id_objeto: int, cantidad: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"INSERT INTO objetos_de_entrenadoc (nombre_entrenador, id_entrenador, nombre_objeto, id_objeto, cantidad) VALUES ('{nombre_entrenador}', {id_entrenador}, '{nombre_objeto}', {id_objeto}, {cantidad})")
    mydb.commit()
    mydb.close()
    return {"message": "Object created successfully"}

# Modify a trainer object
@app.put("/modificar_objeto_de_entrenador")
def modificar_objeto_de_entrenador(id_entrenador: int, id_objeto: int, cantidad: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE objetos_de_entrenadoc SET cantidad = {cantidad} WHERE id_entrenador = {id_entrenador} AND id_objeto = {id_objeto}")
    mydb.commit()
    mydb.close()
    return {"message": "Object modified successfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
