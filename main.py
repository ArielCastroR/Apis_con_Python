from fastapi import FastAPI, HTTPException, status
app = FastAPI()

tasks = []

@app.get('/tasks')
def get_tasks():
    return tasks

@app.post('/tasks')
def post_tasks(task:str,completed:bool=False):
    new_task = {
        "id": len(tasks)+1,
        "task": task,
        "completed": completed
    }
    tasks.append(new_task)
    return {"message":"Insertado correctamente"}

@app.put('/tasks/{task_id}')
def put_tasks(task_id:int, task:str,completed:bool=False):
    for task_item in tasks:
        if task_item["id"] == task_id:
            task_item["task"]= task
            task_item["completed"]=completed
            return {"message": "Task actualizado correctamente"}
    else:
        return {"message": "Id no encontrado"}  

@app.delete('/tasks/{task_id}')
def delete_tasks(task_id:int):
    for task_item in tasks:
        if task_item["id"] == task_id:
            tasks.remove(task_item)
            return {"message": "Task borrada correctamente"}
    else:
        return {"message": "Id no encontrado"} 