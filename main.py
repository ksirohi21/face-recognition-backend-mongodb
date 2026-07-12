from fastapi import FastAPI, UploadFile, File, Form
from database import users_collection, attendance_collection
from face_recognition import find_match
from datetime import datetime
import shutil
import os

app = FastAPI()

os.makedirs("uploads", exist_ok=True)


@app.get("/")
def home():
    return {"message": "Face Recognition Backend Running"}


@app.get("/test-db")
def test_database():
    try:
        users_collection.find_one()
        return {"message": "MongoDB Connected Successfully"}
    except Exception as e:
        return {"message": str(e)}


@app.post("/register")
def register_user(
    name: str = Form(...),
    image: UploadFile = File(...)
):

    file_path = f"uploads/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    users_collection.insert_one({
        "name": name,
        "face_image": file_path
    })

    return {"message": "User Registered Successfully"}


@app.post("/mark-attendance")
def mark_attendance(name: str):

    attendance_collection.insert_one({
        "name": name,
        "date_time": datetime.now(),
        "status": "Present"
    })

    return {"message": "Attendance Marked Successfully"}


@app.post("/recognize")
def recognize_face(image: UploadFile = File(...)):

    path = f"uploads/test_{image.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    match = find_match(path)

    if match:
        return {
            "message": "Face Matched",
            "user_image": match
        }

    return {
        "message": "Face Not Found"
    }