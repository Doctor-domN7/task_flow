import uvicorn

from database import SessionLocal
from db_models import TaskDB

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

from pydantic import BaseModel
from uuid import uuid4

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: str
    title: str 
    completed: bool = False 

class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategoryCreate(BaseModel):
    name: str 

class Category(BaseModel):
    id: str 
    name: str

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

tasks = []
categories = []

@app.get("/tasks",status_code=status.HTTP_200_OK) 
async def get_tasks() -> list[Task]:
    return tasks

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: Session=Depends(get_db)) -> Task:
    task = TaskDB(
        id=str(uuid4()),
        title=payload.title,
        completed=False,
    )

    db.add(task)
    db.commit()

    return task

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: str, payload: TaskUpdate) -> Task:
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None: 
                task.title = payload.title
            if payload.completed is not None: 
                task.completed = payload.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str) -> None:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/categories", status_code=status.HTTP_200_OK)
async def get_categories() -> list[Category]:
    return categories

@app.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate) -> Category:
    category = Category(id=str(uuid4()), name=payload.name)
    categories.append(category)
    return category

@app.patch("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def update_category(category_id: str, payload: CategoryUpdate) -> Category:
    for category in categories:
        if category.id == category_id:
            if payload.name is not None: 
                category.name = payload.name
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: str) -> None:
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(status_code=404, detail="Category not found")          


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)