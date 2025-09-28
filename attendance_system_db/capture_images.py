import cv2
import os
import sqlite3

DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"
DATASET_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\dataset"

def get_student_name(student_id):
    """Fetch student name from DB using student_id"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM students WHERE id=?", (student_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None

def capture_images(student_id, num_samples=20):
    name = get_student_name(student_id)
    if not name:
        print(f"❌ No student found with ID {student_id}")
        return

    # Create dataset folder for student
    student_dir = os.path.join(DATASET_PATH, name)
    os.makedirs(student_dir, exist_ok=True)

    # Open camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW improves Windows webcam detection
    if not cap.isOpened():
        print("❌ Camera not detected. Please check your webcam.")
        return

    count = 0
    print(f"📷 Capturing {num_samples} images for {name}. Press 'q' to quit early.")

    cv2.namedWindow("Capture Images", cv2.WINDOW_NORMAL)  # Window adjustable

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame from camera")
            break

        count += 1
        # Save image automatically
        img_path = os.path.join(student_dir, f"{name}_{count:03d}.jpg")
        cv2.imwrite(img_path, frame)

        # Show counter on frame
        cv2.putText(frame, f"Capturing {count}/{num_samples}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Capture Images", frame)

        # 100ms delay so window renders properly
        key = cv2.waitKey(100) & 0xFF
        if key == ord("q"):  # Press 'q' to quit early
            break
        if count >= num_samples:  # Stop after desired number of samples
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Extra line to close window cleanly
    print(f"✅ Saved {count} images to {student_dir}")

if __name__ == "__main__":
    try:
        student_id = int(input("Enter Student ID: "))
        capture_images(student_id, num_samples=20)
    except ValueError:
        print("❌ Invalid Student ID. Please enter a number.")
