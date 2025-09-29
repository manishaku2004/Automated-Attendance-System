import sqlite3

DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"
DATASET_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\dataset"

def add_student(name, roll_no, department):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (name, roll_no, department) VALUES (?, ?, ?)",
                  (name, roll_no, department))
        conn.commit()
        print(f"✅ Student '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"⚠️ Student with name '{name}' already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    name = input("Enter student name: ")
    roll_no = input("Enter Roll Number: ")
    department = input("Enter department: ")

    add_student(name, roll_no, department)
