import cv2
import face_recognition
import pickle
import mysql.connector
from datetime import datetime

# -------------------------------
# Load encodings
# -------------------------------
print("[INFO] Loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

# -------------------------------
# Connect to database
# -------------------------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # अगर password है तो डालो
        database="attendance_system_db"
    )
    cursor = conn.cursor()
    print("[✅] Database connected successfully!")
except mysql.connector.Error as e:
    print(f"[❌] Database connection error: {e}")
    exit()

# -------------------------------
# Create attendance table if not exists
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255),
    roll_number VARCHAR(50),
    department VARCHAR(100),
    date DATE,
    time TIME
)
""")
conn.commit()

# -------------------------------
# Webcam start
# -------------------------------
print("[INFO] Starting video stream...")
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret or frame is None:
        print("[❌] Failed to grab frame from camera.")
        break

    # Convert safely to RGB
    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f"[❌] Frame conversion error: {e}")
        continue

    # Detect faces
    boxes = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            # -------------------------------
            # Save attendance in DB
            # -------------------------------
            cursor.execute("SELECT roll_number, department FROM students WHERE name=%s", (name,))
            result = cursor.fetchone()
            if result:
                roll, dept = result
                today = datetime.now().date()
                current_time = datetime.now().time()

                # Check if already marked today
                cursor.execute("SELECT * FROM attendance WHERE student_name=%s AND date=%s", (name, today))
                already = cursor.fetchone()

                if not already:
                    cursor.execute("""
                        INSERT INTO attendance (student_name, roll_number, department, date, time)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (name, roll, dept, today, current_time))
                    conn.commit()
                    print(f"[✔] Attendance marked for {name} ({roll}) at {current_time}")
                else:
                    print(f"[ℹ] {name} already marked today.")

        names.append(name)

    # Display names on frame
    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow("Attendance System", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()
