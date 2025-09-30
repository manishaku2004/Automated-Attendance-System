import face_recognition
import cv2
import os
import pickle
import sqlite3

# Database path
DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"

# Dataset folder path
DATASET_PATH = "dataset"

# Output pickle file
ENCODINGS_PATH = "encodings.pickle"

print("[INFO] Loading student data from database...")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT name FROM students")
students = [row[0] for row in c.fetchall()]
conn.close()

print(f"[INFO] Found {len(students)} students in database.")

knownEncodings = []
knownNames = []

for student in students:
    student_folder = os.path.join(DATASET_PATH, student)
    
    if not os.path.exists(student_folder):
        print(f"[WARNING] No images found for {student}, skipping...")
        continue

    for image_name in os.listdir(student_folder):
        image_path = os.path.join(student_folder, image_name)

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"[ERROR] Could not read {image_path}, skipping...")
            continue

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        boxes = face_recognition.face_locations(rgb, model="hog")

        # Compute encodings
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(student)

    print(f"[INFO] Processed images for {student}")

# Save encodings to pickle
print(f"[INFO] Serializing encodings to {ENCODINGS_PATH}...")
data = {"encodings": knownEncodings, "names": knownNames}
with open(ENCODINGS_PATH, "wb") as f:
    f.write(pickle.dumps(data))

print("[✅] Encoding complete! Encodings saved to encodings.pickle")
