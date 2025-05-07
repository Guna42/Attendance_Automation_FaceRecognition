# 🚀 SRM AP - Attendance Automation System

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🌟 Overview
SRM AP is an advanced attendance management system for SRM University AP, using face recognition to automate attendance tracking. Built with Flask, it offers secure OTP login, real-time attendance logging, and absentee email notifications.

## ✨ Features
- 🖼️ **Face Recognition**: Identifies individuals using `face_recognition`.
- 🔒 **OTP Login**: Secure teacher login via email OTP.
- ⏱️ **Real-Time Tracking**: Logs attendance in Excel with timestamps.
- 📧 **Absentee Emails**: Sends notifications to absent students.
- 🌐 **Web UI**: Pages for login, home, scanning, and attendance.
- 🛠️ **Session Control**: Prevents duplicate attendance per session.

## 📸 Screenshots
The following screenshots are located in the `screenshots/` folder of the project directory and are displayed below.

**Login Page**  
![Login Page](screenshots/Login.png)

**Home Page**  
![Home Page](screenshots/home.png)

**Scan & Mark**  
![Scan & Mark](screenshots/detect%20(1).png)

**Attendance**  
![Attendance](screenshots/check%26mail.png)

## 🛠️ Requirements
- Python 3.8+
- Flask: `pip install flask`
- OpenCV: `pip install opencv-python`
- Face Recognition: `pip install face_recognition`
- Flask-Mail: `pip install flask-mail`
- SQLite3 (built-in)
- OpenPyXL: `pip install openpyxl`
- NumPy: `pip install numpy`
- Webcam

## 🔧 Setup
1. **Clone Repository (if applicable)**:
   ```bash
   git clone https://github.com/Guna42/Attendance_Automation_FaceRecognition.git
   cd Attendance_Automation_FaceRecognition
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Email**:
   Update `face_recognition_live.py`:
   ```python
   app.config['MAIL_SERVER'] = 'smtp.gmail.com'
   app.config['MAIL_PORT'] = 587
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = "your-email@srmap.edu.in"
   app.config['MAIL_PASSWORD'] = "your-app-password"
   app.config['MAIL_DEFAULT_SENDER'] = "your-email@srmap.edu.in"
   ```

4. **Set Up Database**:
   Ensure `attendance_system.db` exists at the path in the code. Create a `teachers` table with an `email` column.

5. **Prepare Known Faces**:
   Add images to `known_faces` directory and update `known_faces_db` in the code.

6. **Run**:
   ```bash
   python face_recognition_live.py
   ```

7. Access at `http://127.0.0.1:5000`.

## 🚀 Usage
- **Login**: Go to `/`, enter your email, and verify the OTP.
- **Home**: Navigate to `/Home` to choose "Check Attendance" or "Scan & Mark".
- **Scan & Mark**: At `/scan`, click "Start" to scan faces, "Stop" to end.
- **View Attendance**: Check `/attendance` and send absentee emails.
- **Logout**: Close the browser to end the session.

## 📂 File Structure
- `face_recognition_live.py`: Main Flask app.
- `templates/`: HTML templates.
- `static/`: CSS, JS, images.
- `screenshots/`: Add your screenshots here.
- `known_faces/`: Images for face recognition.
- `attendance.xlsx`: Attendance logs.
- `present_students.xlsx`: Present students.
- `absent_students.xlsx`: Absent students.
- `attendance_system.db`: SQLite database.

## 📝 Notes
- Ensure webcam connectivity.
- Tune `process_every_n_frames` for performance.
- Attendance files reset on startup.
- Adjust face recognition threshold and margin as needed.

## 🤝 Contributing
Fork, make changes, and submit a pull request.

## 📜 License
MIT License. See `LICENSE` file.

## 🙌 Acknowledgments
- Uses `face_recognition` library.
- Built with Flask and SQLite.
- Developed at SRM University AP.
