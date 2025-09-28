import sqlite3
import os

# Absolute path (अपना सही path डालें)
DB_PATH = r"C:\xampp\htdocs\automated attendance system\attendance_system_db\database\students.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT * FROM students")
rows = c.fetchall()

print("👩‍🎓 Students in Database:")
for row in rows:
    print(row)

conn.close()
