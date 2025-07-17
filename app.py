from flask import Flask, request
import mysql.connector

app = Flask(__name__)


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="#MySQL",
    database="ussd_university_system",
    auth_plugin='mysql_native_password'
)

@app.route('/ussd', methods=['POST'])
def ussd_callback():
    session_id = request.values.get('sessionId')
    service_code = request.values.get('serviceCode')
    phone_number = request.values.get('phoneNumber')
    text = request.values.get('text', '')

    
    print(f"Raw phone number: '{phone_number}'")
    if phone_number:
        phone_number = phone_number.replace("+", "").replace(" ", "")
        if phone_number.startswith("0"):
            phone_number = "254" + phone_number[1:]
        print(f"Normalized phone number: '{phone_number}'")

    
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, student_id FROM students WHERE phone_number = %s", (phone_number,))
    student = cursor.fetchone()
    cursor.close()

    if not student:
        return "END Your phone number is not registered. Please contact admin.", 200, {'content-type': 'text/plain'}

    student_name, student_id = student
    response = ""


    if text == "":
        response = f"CON Welcome to UniConnect, {student_name}\n"
        response += "1. View Results\n"
        response += "2. Check Balance\n"
        response += "3. View Timetable\n"
        response += "4. Missed Exams\n"
        response += "5. Notifications\n"
        response += "6. Exit"

    elif text == "1":
        response = "CON View Results\n1. Current Term\n2. Previous Terms"

    elif text == "1*1":
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT course_name, course_code, grade, term 
                FROM results 
                WHERE student_id = %s AND term = '2024 Term 1'
            """, (student_id,))
            rows = cursor.fetchall()
        if rows:
            response = "END Current Term Results:\n"
            for row in rows:
                response += f"{row[0]} ({row[1]}): {row[2]}, {row[3]}\n"
        else:
            response = "END No results found for current term."

    elif text == "1*2":
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT course_name, course_code, grade, term 
                FROM results 
                WHERE student_id = %s AND term != '2024 Term 1'
            """, (student_id,))
            rows = cursor.fetchall()
        if rows:
            response = "END Previous Term Results:\n"
            for row in rows:
                response += f"{row[0]} ({row[1]}): {row[2]}, {row[3]}\n"
        else:
            response = "END No previous term results found."

    elif text == "2":
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT term, amount_due, amount_paid, balance
                FROM fees
                WHERE student_id = %s
            """, (student_id,))
            balance_info = cursor.fetchone()

        if balance_info:
            term, due, paid, bal = balance_info
            response = "END Fee Balance\n"
            response += f"Term: {term}\n"
            response += f"Amount Due: KES {due}\n"
            response += f"Amount Paid: KES {paid}\n"
            response += f"Balance: KES {bal}\n"
        else:
            response = "END Balance info not found."

    elif text == "3":
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT day_of_week, course_name, start_time, end_time, venue
                FROM timetable
                WHERE student_id = %s
                ORDER BY FIELD(day_of_week, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
            """, (student_id,))
            timetable = cursor.fetchall()

        if timetable:
            response = "END Your Timetable:\n"
            for row in timetable:
                day, course, start, end, venue = row
                response += f"{day}: {course}\n{start} - {end} at {venue}\n"
        else:
            response = "END No timetable found."

    elif text == "4":
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT course_code, course_name, date
                FROM missed_exams
                WHERE student_id = %s
            """, (student_id,))
            missed = cursor.fetchall()

        if missed:
            response = "END Missed Exams:\n"
            for row in missed:
                code, name, date = row
                response += f"{code} - {name}\nReschedule: {date}\n\n"
        else:
            response = "END No missed exams found."

    elif text == "5":
        with conn.cursor() as cursor:
            cursor.execute("SELECT title, message FROM notifications")
            notifications = cursor.fetchall()
        if notifications:
            response = "END Notifications:\n"
            for note in notifications:
                response += f"- {note[0]}: {note[1]}\n"
        else:
            response = "END You have no new notifications."

    elif text == "6":
        response = "END Thank you for using UniConnect. Goodbye!"

    else:
        response = "END Invalid option. Please try again."

    return response, 200, {'content-type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)

# USSD BACKEND created by ENG. Esther Maina | 2025 | For Educational/demo use only~