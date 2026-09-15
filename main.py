from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Todo API")


class TaskCreate(BaseModel):
    title: str


tasks = []
next_id = 1


@app.get("/")
def root():
    return {"message": "Todo API is running"}


@app.post("/tasks")
def add_task(task: TaskCreate):
    global next_id

    new_task = {
        "id": next_id,
        "title": task.title,
        "completed": False
    }

    tasks.append(new_task)
    next_id += 1

    return new_task


@app.get("/tasks")
def list_tasks():
    return tasks


@app.patch("/tasks/{task_id}/done")
def mark_task_done(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task

    raise HTTPException(status_code=404, detail="Task not found")




