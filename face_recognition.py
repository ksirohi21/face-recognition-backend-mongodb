from deepface import DeepFace
import os


def verify_face(img1, img2):

    try:
        print("VERIFYING:", img1, img2)
        result = DeepFace.verify(
    img1_path=img1,
    img2_path=img2,
    model_name="Facenet512",
    detector_backend="opencv",
    enforce_detection=True
)

        print("RESULT:", result)
        print("VERIFIED VALUE:", result["verified"])

        return result["verified"]

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
        if file.lower() == "icon.jpg":
            continue

        saved_image = os.path.join(folder, file)

        try:
            if verify_face(test_image, saved_image):
                return file

        except Exception as e:
            print("DeepFace Error:", file, e)

    return None