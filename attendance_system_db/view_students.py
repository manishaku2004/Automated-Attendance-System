import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"
DATASET_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\dataset"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT * FROM students")
rows = c.fetchall()

print("👩‍🎓 Students in database:")
for row in rows:
    print(row)

conn.close()
