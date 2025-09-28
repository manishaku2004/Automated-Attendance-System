import sqlite3
import os

# अगर database फोल्डर नहीं है तो बना लो
os.makedirs("database", exist_ok=True)

# Database file का path
db_path = "database/students.db"

# Connection open करो
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Students table: यहाँ basic student info store होगा
c.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    roll_no TEXT NOT NULL,
    department TEXT
)
''')

# Attendance table: यहाँ रोज़ attendance mark होगा
c.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

# Save & close
conn.commit()
conn.close()

print(f"Database created successfully at: {db_path}")
