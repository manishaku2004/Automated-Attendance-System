import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          # XAMPP का default user
        password="",          # अगर password set किया है तो यहाँ लिखें
        database="attendance_system_db"
    )

    cursor = conn.cursor()
    print("[✅] Database connected successfully!")

except mysql.connector.Error as e:
    print(f"[❌] Database connection error: {e}")
