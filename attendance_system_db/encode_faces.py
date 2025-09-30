import cv2
import os
import face_recognition
import pickle
import mysql.connector

# ------------------ Database Config ------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "attendance_system"

# ------------------ Dataset Path ---------------------
DATASET_PATH = "dataset"

# ------------------ Output File ----------------------
ENCODINGS_FILE = "encodings.pickle"

def get_students_from_db():
    """Fetch all students from database"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, roll_number FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        return students
    except Exception as e:
        print("[❌] Database connection error:", e)
        return []


def encode_faces():
    print("[INFO] Loading student data from database...")
    students = get_students_from_db()
    print(f"[INFO] Found {len(students)} students in database.")

    knownEncodings = []
    knownNames = []

    for student in students:
        name = student[0]  # student name (same as folder name in dataset)
        student_folder = os.path.join(DATASET_PATH, name)

        if not os.path.exists(student_folder):
            print(f"[WARNING] No folder found for {name}, skipping...")
            continue

        print(f"[INFO] Processing images for {name}...")

        for img_name in os.listdir(student_folder):
            img_path = os.path.join(student_folder, img_name)

            # load image
            image = cv2.imread(img_path)
            if image is None:
                print(f"[WARNING] Could not load {img_path}, skipping...")
                continue

            # convert to RGB
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect face locations
            boxes = face_recognition.face_locations(rgb, model="hog")

            # encode the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

    # save encodings
    print(f"[INFO] Serializing encodings to {ENCODINGS_FILE}...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open(ENCODINGS_FILE, "wb") as f:
        f.write(pickle.dumps(data))

    print("[✅] Encoding complete! Encodings saved to encodings.pickle")


if __name__ == "__main__":
    encode_faces()
