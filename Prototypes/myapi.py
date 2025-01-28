from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "Vedant",
        "age": 26,
        "class": "MS IS"
    },
    2: {
        "name": "Abhinav",
        "age": 27,
        "class": "MS IS"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

@app.get("/")
def index():
    return {"name": "First Data"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of Student you want to view", gt=0, le=2)):
    return students[student_id]

@app.get("/get-by-name")
def get_student(*, name: Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"} 
