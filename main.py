from fastapi import FastAPI
from database import get_connection
from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from database import get_connection
from face_recognition import find_match
from fastapi import UploadFile, File
import shutil
import os
app = FastAPI()
os.makedirs("uploads", exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Face Recognition Backend Running"
    }


@app.get("/test-db")
def test_database():

    connection = get_connection()

    if connection:
        return {
            "message": "MySQL Connected Successfully"
        }

    return {
        "message": "Database Connection Failed"
    }
@app.post("/register")
def register_user(
    name: str = Form(...),
    image: UploadFile = File(...)
):

    file_path = f"uploads/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users(name, face_image)
    VALUES(%s, %s)
    """

    cursor.execute(query, (name, file_path))

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User Registered Successfully"
    }
from datetime import datetime

@app.post("/mark-attendance")
def mark_attendance(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO attendance(user_id, date_time, status)
    VALUES(%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            user_id,
            datetime.now(),
            "Present"
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Attendance Marked Successfully"
    }

@app.post("/recognize")
def recognize_face(image: UploadFile = File(...)):

    path = f"uploads/test_{image.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    print("TEST IMAGE PATH:", path)
    print("FILE EXISTS:", os.path.exists(path))

    match = find_match(path)

    if match:
        return {
            "message": "Face Matched",
            "user_image": match
        }

    return {
        "message": "Face Not Found"
    }