import csv
import os

def split_attendance(current_session_id, known_faces_db):
    # File paths
    attendance_file = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\attendance.csv"
    present_file = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\present_students.csv"
    absent_file = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\absent_students.csv"

    # Get present students from attendance.csv for current session
    present_students = set()
    if os.path.exists(attendance_file):
        with open(attendance_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["SessionID"] == current_session_id:
                    present_students.add(row["Name"])

    # Get all students from known_faces_db
    all_students = {details["name"]: details["email"] for details in known_faces_db.values()}

    # Absentees = all students - present students
    absent_students = {name: email for name, email in all_students.items() if name not in present_students}

    # Write present students
    with open(present_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Status"])
        for name in present_students:
            email = all_students[name]
            writer.writerow([name, email, "Present"])

    # Write absent students
    with open(absent_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Status"])
        for name, email in absent_students.items():
            writer.writerow([name, email, "Absent"])

    print(f"Attendance split: {len(present_students)} present, {len(absent_students)} absent")

if __name__ == "__main__":
    # This is just for testing standalone; we'll call it from face_recognition_live.py
    sample_session_id = "test_session"
    sample_db = {
        "kartheek.jpg": {"name": "Kartheek Sanka", "email": "kartheek.reddy@example.com"},
        "sumanth.jpg": {"name": "Sumanth ", "email": "sumanth.kumar@example.com"}
    }
    split_attendance(sample_session_id, sample_db)