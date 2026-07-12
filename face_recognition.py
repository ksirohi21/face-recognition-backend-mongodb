import face_recognition
import os


def verify_face(img1, img2):
    try:
        print("VERIFYING:", img1, img2)

        image1 = face_recognition.load_image_file(img1)
        image2 = face_recognition.load_image_file(img2)

        enc1 = face_recognition.face_encodings(image1)
        enc2 = face_recognition.face_encodings(image2)

        if len(enc1) == 0 or len(enc2) == 0:
            print("Face not detected")
            return False

        result = face_recognition.compare_faces([enc2[0]], enc1[0])

        print("RESULT:", result)

        return result[0]

    except Exception as e:
        print("VERIFY ERROR:", e)
        return False


def find_match(test_image):

    folder = "uploads"

    if not os.path.exists(folder):
        return None

    print("UPLOAD FILES:", os.listdir(folder))

    for file in os.listdir(folder):

        if file.startswith("test_"):
            continue

        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        saved_image = os.path.join(folder, file)

        if verify_face(test_image, saved_image):
            return file

    return None