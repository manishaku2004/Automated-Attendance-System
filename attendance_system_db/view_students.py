import mysql.connector

def view_students():
    try:
        # MySQL connection
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # अगर root पर password है तो डालो
            database="attendance_system_db"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()

        print("👩‍🎓 Students in database:")
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"[❌] Database error: {err}")

if __name__ == "__main__":
    view_students()
