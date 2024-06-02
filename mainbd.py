from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2

app = FastAPI()

db_params = {
    'dbname': 'my_collections',
    'user': 'postgres',
    'password': 'contrasena',
    'host': 'localhost',
    'port': '5432',
}

conn = psycopg2.connect(**db_params)

class Tarea(BaseModel):
    table_name: str
    autor: str
    fecha_estreno: str

class Tarea2(BaseModel):
    id: str
    autor: str


temporal_list = []

@app.get('/tarea')
def get_tarea():    
    with conn.cursor() as cursor:        
        try:
            get_data_query = '''
            SELECT * FROM my_movies
            '''
            cursor.execute(get_data_query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
                temporal_list.append(row)
        except:
            print("Error con la consulta GET")
    return {"message": temporal_list}

                
@app.post('/tarea')
def create_task(tabla:Tarea):
    with conn.cursor() as cursor:       
        try:
            queryid = '''
            SELECT max(id) FROM my_movies
            '''
            cursor.execute(queryid)
            rows = cursor.fetchall()
            a=rows[0] 
            b=int(a[0])
            insert_data_query = f'''
            INSERT INTO {tabla.table_name} (id, autor, fecha_estreno) VALUES ( {b+1}, %s, %s);
            '''
            data_to_insert = (tabla.autor, tabla.fecha_estreno)
            cursor.execute(insert_data_query,data_to_insert )
            conn.commit()
        except Exception as e:
            print(e)
            print("Error con la consulta POST")
    return {"message": "Creado correctamente"}


@app.put('/tarea')
def put_tasks(id:int, autor:str):
    with conn.cursor() as cursor:        
        try:
            data_query = f'''
            UPDATE my_movies SET autor='{autor}' where id={id}
            '''            
            cursor.execute(data_query)
            conn.commit()
        except:
            print("Error con la consulta PUT")
    return {"message": "Modificado Correctamente"}



@app.delete('/tarea')
def delete_tasks(id:int):
    with conn.cursor() as cursor:        
        try:
            data_query = f'''
            DELETE FROM my_movies where id={id}
            '''            
            cursor.execute(data_query)
            conn.commit()
        except:
            print("Error con la consulta PUT")
    return {"message": "Modificado Correctamente"}