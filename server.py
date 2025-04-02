import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime
from flask import Flask, Response, jsonify, render_template, request, send_from_directory
from flask_mail import Mail, Message
import sqlite3
import random

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.urandom(24)  # Secret key for session management

# Database connection for OTP (teachers table)
def get_db_connection():
    conn = sqlite3.connect(r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\attendance_system.db")
    conn.row_factory = sqlite3.Row
    return conn

# Mail configuration for OTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "yashwanth_seeram@srmap.edu.in"  # Replace with your Gmail
app.config['MAIL_PASSWORD'] = "cabr ymzw meda lrud"  # Replace with App Password
app.config['MAIL_DEFAULT_SENDER'] = "yashwanth_seeram@srmap.edu.in"
mail = Mail(app)

# Store OTPs temporarily
otp_storage = {}

# Simulated face database
known_faces_db = {
    "kartheek.jpg": {"name": "Kartheek Sanka", "email": "kartheek.reddy@example.com"},
    "sumanth.jpg": {"name": "Sumanth ", "email": "sumanth.kumar@example.com"},
    "Guna.jpg": {"name": "Guna vardhan", "email": "gunavardhan779@gmail.com"},
    "yaswanth.jpg": {"name": "Yaswanth ", "email": "yaswanth.patel@example.com"}
}

# Load known face images and compute encodings
known_faces_dir = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\known_faces"
known_face_encodings = {}
for filename in os.listdir(known_faces_dir):
    if filename in known_faces_db:
        img_path = os.path.join(known_faces_dir, filename)
        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)
        if len(encodings) > 0:
            known_face_encodings[filename] = encodings[0]
            print(f"Loaded encoding for {filename}")
        else:
            print(f"Warning: No face detected in {filename}")

# Initialize attendance log
attendance_file = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\attendance.csv"
attendance_marked = set()

if not os.path.exists(attendance_file):
    with open(attendance_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Email", "Timestamp", "Status"])

def mark_attendance(name, email):
    if name != "Unknown" and name not in attendance_marked:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(attendance_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, timestamp, "Present"])
        attendance_marked.add(name)
        print(f"Marked attendance for {name} at {timestamp}")

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

last_matches = []
last_matched_name = "Unknown"
last_face_location = None
frame_count = 0
process_every_n_frames = 3
is_running = False

def generate_frames():
    global last_matches, last_matched_name, last_face_location, frame_count, is_running
    while True:
        if not is_running:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Face Recognition Stopped", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            continue

        ret, frame = cap.read()
        if not ret or frame is None:
            print("Warning: Failed to capture frame.")
            continue

        frame_count += 1
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        if frame_count % process_every_n_frames == 0:
            face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_locations = [(top * 2, right * 2, bottom * 2, left * 2) for (top, right, bottom, left) in face_locations]

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                distances = []
                for filename, known_encoding in known_face_encodings.items():
                    distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
                    name = known_faces_db[filename]["name"]
                    distances.append((distance, name))

                distances.sort()
                min_distance, matched_name = distances[0]
                threshold = 0.6
                margin = 0.1

                if min_distance < threshold and (len(distances) == 1 or distances[1][0] - min_distance > margin):
                    matched_name = distances[0][1]
                else:
                    matched_name = "Unknown"

                last_matches.append(matched_name)
                if len(last_matches) > 10:
                    last_matches.pop(0)
                if last_matches.count("Unknown") < 6 and len(last_matches) == 10:
                    matched_name = max(set(last_matches), key=last_matches.count)

                if matched_name != "Unknown":
                    email = known_faces_db[[k for k, v in known_faces_db.items() if v["name"] == matched_name][0]]["email"]
                    mark_attendance(matched_name, email)

                last_matched_name = matched_name
                last_face_location = (top, right, bottom, left)

        if last_face_location is not None:
            top, right, bottom, left = last_face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{last_matched_name} (Dist: {min_distance:.2f})", (left, top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/Home')
def home():
    return render_template('Home.html')

@app.route('/scan')
def scan():
    return render_template('scan&mark.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    global is_running
    is_running = True
    print("Face recognition started.")
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    global is_running
    is_running = False
    print("Face recognition stopped.")
    return jsonify({"status": "stopped"})

@app.route('/attendance_data')
def attendance_data():
    attendance_list = []
    with open(attendance_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            attendance_list.append(row)
    return jsonify(attendance_list)

# OTP Routes
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM teachers WHERE email = ?", (email,))
    teacher = cursor.fetchone()
    conn.close()

    if not teacher:
        return jsonify({"error": "Email not registered"}), 400

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp

    try:
        msg = Message("Your OTP for Login", recipients=[email])
        msg.body = f"Your OTP is: {otp}. It is valid for 5 minutes."
        mail.send(msg)
        return jsonify({"message": "OTP sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send OTP: {str(e)}"}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get("email")
    entered_otp = data.get("otp")

    if not email or not entered_otp:
        return jsonify({"error": "Email and OTP are required"}), 400

    if email in otp_storage and otp_storage[email] == entered_otp:
        del otp_storage[email]
        return jsonify({"message": "OTP verified successfully", "redirect": "/Home"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)