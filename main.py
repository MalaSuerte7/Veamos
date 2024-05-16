from fastapi import FastAPI
import mysql.connector
import schemas

app = FastAPI()

# Database connection information
host_name = "34.239.20.242"
port_number = "8005"
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "entrenadores"

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
def add_trainer(item: schemas.Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre = item.nombre
    apellido = item.apellido
    medallas = item.medallas
    fecha_nacimiento = item.fecha_nacimiento
    edad = item.edad
    cursor = mydb.cursor()
    sql = "INSERT INTO entrenadores (nombre, apellido, medallas, fecha_nacimiento, edad) VALUES (%s, %s, %s, %s, %s)"
    val = (nombre, apellido, medallas, fecha_nacimiento, edad)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Trainer added successfully"}

# Modify a trainer
@app.put("/trainers/{id}")
def update_trainer(id: int, item: schemas.Trainer):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    nombre = item.nombre
    apellido = item.apellido
    medallas = item.medallas
    fecha_nacimiento = item.fecha_nacimiento
    edad = item.edad
    cursor = mydb.cursor()
    sql = "UPDATE entrenadores SET nombre=%s, apellido=%s, medallas=%s, fecha_nacimiento=%s, edad=%s WHERE entrenador_id=%s"
    val = (nombre, apellido, medallas, fecha_nacimiento, edad, id)
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
