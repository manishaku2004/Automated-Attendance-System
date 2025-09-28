import cv2
import os
import sqlite3
DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"
DATASET_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\dataset"

def get_student_name(student_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM students WHERE id=?", (student_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def capture_images(student_id, num_samples=20):
    name = get_student_name(student_id)
    if not name:
        print(f"❌ No student found with ID {student_id}")
        return

    student_dir = os.path.join(DATASET_PATH, name)
    os.makedirs(student_dir, exist_ok=True)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ Camera not detected. Please check your webcam.")
        return

    count = 0
    print(f"📷 Capturing {num_samples} images for {name}. Press 'q' to quit early.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame from camera")
            break

        count += 1
        img_path = os.path.join(student_dir, f"{name}_{count:03d}.jpg")
        cv2.imwrite(img_path, frame)

        cv2.putText(frame, f"Capturing {count}/{num_samples}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Capture Images", frame)

        # यहाँ 100ms wait रखा है ताकि window properly render हो
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break
        if count >= num_samples:
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # 🔑 extra line so window closes cleanly
    print(f"✅ Saved {count} images to {student_dir}")

if __name__ == "__main__":
    try:
        student_id = int(input("Enter Student ID: "))
        capture_images(student_id, num_samples=20)
    except ValueError:
        print("❌ Invalid Student ID. Please enter a number.")
