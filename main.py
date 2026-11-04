from sqlalchemy import select
import uvicorn

from db_models import CategoryDB, TaskDB

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from pydantic import BaseModel, ConfigDict
from uuid import uuid4

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: str
    title: str 
    completed: bool = False 
    model_config = ConfigDict(from_attributes=True)

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategoryCreate(BaseModel):
    name: str 

class Category(BaseModel):
    id: str 
    name: str
    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    name: str | None = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tasks",status_code=status.HTTP_200_OK) 
def get_tasks(db: Session=Depends(get_db)) -> list[Task]:
    tasks = db.scalars(select(TaskDB)).all()
    return tasks

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session=Depends(get_db)) -> Task:
    task = TaskDB(
        id=str(uuid4()),
        title=payload.title,
        completed=False,
    )

    db.add(task)
    db.commit()

    return task

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task(task_id: str, payload: TaskUpdate, db: Session=Depends(get_db)) -> Task:
    task = db.get(TaskDB, task_id)
    if task is None: 
        raise HTTPException(status_code=404, detail="Task not found")
        
    task.title = payload.title if payload.title is not None else task.title
    task.completed = payload.completed if payload.completed is not None else task.completed

    db.commit()
    return task
    

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session=Depends(get_db)) -> None:
    task = db.get(TaskDB, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    db.delete(task)
    db.commit()


@app.get("/categories", status_code=status.HTTP_200_OK)
def get_categories(db: Session=Depends(get_db)) -> list[Category]:
    categories = db.scalars(select(CategoryDB)).all()
    return categories

@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session=Depends(get_db)) -> Category:
    category = CategoryDB(id=str(uuid4()), name=payload.name)
    
    db.add(category)
    db.commit()

    return category

@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
def update_category(category_id: str, payload: CategoryUpdate, db: Session=Depends(get_db)) -> Category:
    category = db.get(CategoryDB, category_id)
    if category is None: 
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = payload.name if payload.name is not None else category.name

    db.commit()

    return category
    

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session=Depends(get_db)) -> None:
    category = db.get(CategoryDB, category_id)

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()



if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)