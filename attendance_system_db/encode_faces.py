import cv2
import os
import face_recognition
import pickle
import mysql.connector

# ------------------ Database Config ------------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""  # अगर password है तो यहाँ लिखें
DB_NAME = "attendance_system_db"

# ------------------ Dataset Path ---------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "dataset")

# ------------------ Output File ----------------------
ENCODINGS_FILE = os.path.join(BASE_DIR, "encodings.pickle")

# 🔹 Fetch students from MySQL
def get_students_from_db():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        print("[✅] Database connected successfully!")
        return students
    except mysql.connector.Error as e:
        print(f"[❌] Database connection error: {e}")
        return []

# 🔹 Encode faces
def encode_faces():
    print("[INFO] Loading student data from database...")
    students = get_students_from_db()
    print(f"[INFO] Found {len(students)} students in database.")

    knownEncodings = []
    knownNames = []

    for student in students:
        name = student[0].strip()  # Student name
        student_folder = os.path.join(DATASET_PATH, name.replace(" ", "_"))

        if not os.path.exists(student_folder):
            print(f"[WARNING] No folder found for {name}, skipping...")
            continue

        print(f"[INFO] Processing images for {name}...")

        for img_name in os.listdir(student_folder):
            if not img_name.lower().endswith(".jpg"):
                continue  # skip non-jpg files

            img_path = os.path.join(student_folder, img_name)

            # Load image
            image = cv2.imread(img_path)

            if image is None:
                print(f"[WARNING] Could not load {img_path}, skipping...")
                continue

            # Ensure it's uint8
            image = image.astype("uint8")

            # Handle grayscale, RGBA, or BGR correctly
            if len(image.shape) == 2:  # grayscale
                rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[2] == 4:  # RGBA
                rgb = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
            else:  # BGR
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            print(f"[DEBUG] Final RGB image shape={rgb.shape}, dtype={rgb.dtype}")

            # Detect face locations
            boxes = face_recognition.face_locations(rgb, model="hog")

            # Encode faces
            encodings = face_recognition.face_encodings(rgb, boxes)

            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)

    # Save encodings
    print(f"[INFO] Serializing encodings to {ENCODINGS_FILE}...")
    data = {"encodings": knownEncodings, "names": knownNames}
    with open(ENCODINGS_FILE, "wb") as f:
        f.write(pickle.dumps(data))

    print("[✅] Encoding complete! Encodings saved to encodings.pickle")

# ------------------ Main ------------------
if __name__ == "__main__":
    encode_faces()
