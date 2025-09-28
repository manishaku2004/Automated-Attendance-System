# recognize_and_attend.py
import cv2
import face_recognition
import pickle
import os
import csv
from datetime import datetime
import numpy as np

ENCODINGS_PATH = "encodings/encodings.pickle"
ATTENDANCE_CSV = "attendance.csv"
TOLERANCE = 0.5  # smaller -> stricter matching

if not os.path.exists(ENCODINGS_PATH):
    raise FileNotFoundError("Encodings not found. Run encode_faces.py first.")

with open(ENCODINGS_PATH, "rb") as f:
    data = pickle.load(f)
known_encodings = data["encodings"]
known_names = data["names"]

def already_marked(name, date_str):
    if not os.path.exists(ATTENDANCE_CSV):
        return False
    with open(ATTENDANCE_CSV, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3 and row[0] == name and row[1] == date_str:
                return True
    return False

def mark_attendance(name, csv_path=ATTENDANCE_CSV):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    if already_marked(name, date_str):
        return False
    header_needed = not os.path.exists(csv_path)
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["Name", "Date", "Time"])
        writer.writerow([name, date_str, time_str])
    return True

cap = cv2.VideoCapture(0)
print("Press 'q' to quit. Recognizing...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)  # speedup
    rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # compare to known
        distances = face_recognition.face_distance(known_encodings, face_encoding)
        if len(distances) > 0:
            best_idx = np.argmin(distances)
            if distances[best_idx] <= TOLERANCE:
                name = known_names[best_idx]
            else:
                name = "Unknown"
        else:
            name = "Unknown"

        # scale back up locations
        top *= 4; right *= 4; bottom *= 4; left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        if name != "Unknown":
            if mark_attendance(name):
                print(f"Marked attendance for {name} at {datetime.now().strftime('%H:%M:%S')}")
            # else: already marked for today

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
