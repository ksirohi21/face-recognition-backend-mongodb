from pymongo import MongoClient

MONGO_URI = "mongodb+srv://facerecognition:Kartik07@facerecognition.85i4ggh.mongodb.net/?retryWrites=true&w=majority&appName=facerecognition"

client = MongoClient(MONGO_URI)

db = client["face_attendance"]

users_collection = db["users"]
attendance_collection = db["attendance"]