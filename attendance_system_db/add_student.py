import mysql.connector

def add_student():
    # MySQL connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # अगर root पर password set है तो यहाँ डालें
        database="attendance_system_db"
    )
    cursor = conn.cursor()

    # user input
    name = input("Enter student name: ")
    roll_number = input("Enter Roll Number: ")
    department = input("Enter department: ")

    # dataset folder me image का नाम student name के same रखो
    image = f"{name}.jpg"

    # insert query
    query = "INSERT INTO students (name, roll_number, department, image) VALUES (%s, %s, %s, %s)"
    values = (name, roll_number, department, image)

    cursor.execute(query, values)
    conn.commit()

    print(f"✅ Student '{name}' added successfully with image '{image}'")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    add_student()
