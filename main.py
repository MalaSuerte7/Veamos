from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database connection information
host_name = "database-1.crlz1rjtrz0e.us-east-1.rds.amazonaws.com"
port_number = "3306"  # El puerto para MySQL es normalmente 3306, no 8005
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "Train"

# Estructura para representar un entrenador usando Pydantic
class Trainer(BaseModel):
    nombre: str
    apellido: str
    medallas: int
    fecha_nacimiento: str
    edad: int

# Get all trainers
@app.get("/trainers")
def get_trainers():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM entrenadores")
    result = cursor.fetchall()
    mydb.close()
    return {"trainers": result}

# Get a trainer by ID
@app.get("/trainers/{id}")
def get_trainer(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM entrenadores WHERE entrenador_id = {id}")
    result = cursor.fetchone()
    mydb.close()
    return {"trainer": result}

# Add a new trainer
@app.post("/trainers")
def add_trainer(item: Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO entrenadores (nombre, apellido, medallas, fecha_nacimiento, edad) VALUES (%s, %s, %s, %s, %s)"
    val = (item.nombre, item.apellido, item.medallas, item.fecha_nacimiento, item.edad)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Trainer added successfully"}

# Modify a trainer
@app.put("/trainers/{id}")
def update_trainer(id: int, item: Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE entrenadores SET nombre=%s, apellido=%s, medallas=%s, fecha_nacimiento=%s, edad=%s WHERE entrenador_id=%s"
    val = (item.nombre, item.apellido, item.medallas, item.fecha_nacimiento, item.edad, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Trainer modified successfully"}

# Delete a trainer by ID
@app.delete("/trainers/{id}")
def delete_trainer(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM entrenadores WHERE entrenador_id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Trainer deleted successfully"}

# Login
@app.post("/login")
def login(username: str):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM entrenadores WHERE nombre = '{username}'")
    result = cursor.fetchone()
    if result is None:
        cursor.execute(f"INSERT INTO entrenadores (nombre, apellido, medallas, fecha_nacimiento, edad) VALUES ('{username}', 'Apellido', 0, '2000-01-01', 0)")
        cursor.execute(f"SELECT * FROM entrenadores WHERE nombre = '{username}'")
        result = cursor.fetchone()
        cursor.execute(f"INSERT INTO inventarios (entrenador_id, pokebolas, pociones, dinero) VALUES ({result[0]}, 0, 0, 1000)")
        mydb.commit()
    mydb.close()
    return {"trainer": result}

# Get Trainer pokemons
@app.get("/pokemons_de_entrenador")
def get_pokemons_de_entrenador(id_entrenador: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM pokemons_de_entrenador WHERE id_entrenador = {id_entrenador}")
    result = cursor.fetchall()
    mydb.close()
    return {"pokemons": result}

# Create a new pokemon for a trainer
@app.post("/crear_pokemon_de_entrenador")
def crear_pokemon_de_entrenador(id_entrenador: int, id_pokemon: int, nivel: int, experiencia: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"INSERT INTO pokemons_de_entrenador (id_entrenador, id_pokemon, nivel, experiencia) VALUES ({id_entrenador}, {id_pokemon}, {nivel}, {experiencia})")
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon created successfully"}

# Show trainer inventory
@app.get("/objetos_de_entrenador")
def get_objetos_de_entrenador(id_entrenador: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM objetos_de_entrenador WHERE id_entrenador = {id_entrenador}")
    result = cursor.fetchall()
    mydb.close()
    return {"objects": result}

# Create a new object for a trainer
@app.post("/crear_objeto_de_entrenador")
def crear_objeto_de_entrenador(id_entrenador: int, id_objeto: int, cantidad: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO objetos_de_entrenador (id_entrenador, id_objeto, cantidad) VALUES ({id_entrenador}, {id_objeto}, {cantidad})")
    mydb.commit()
    mydb.close()
    return {"message": "Object created successfully"}

# Modify a trainer object
@app.put("/modificar_objeto_de_entrenador")
def modificar_objeto_de_entrenador(id_objeto: int, id_entrenador: int, id_objeto_nuevo: int, cantidad_nueva: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"UPDATE objetos_de_entrenador SET id_objeto={id_objeto_nuevo}, cantidad={cantidad_nueva} WHERE id_objeto={id_objeto} AND id_entrenador={id_entrenador}")
    mydb.commit()
    mydb.close()
    return {"message": "Object modified successfully"}