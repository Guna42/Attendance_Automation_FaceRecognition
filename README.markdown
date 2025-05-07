# 🚀 SRM AP - Attendance Automation System

A modern attendance management system for SRM University AP, leveraging face recognition to streamline attendance tracking. Built with Flask, it offers secure OTP login, real-time logging, and automated absentee notifications.

---

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

---

## 🌟 Overview
SRM AP automates attendance at SRM University AP using advanced face recognition. Powered by Flask, it provides:
- Secure teacher login with email OTP.
- Real-time attendance logging in Excel.
- Automated email notifications for absent students.
- A user-friendly web interface.

---

## ✨ Features
- 🖼️ **Face Recognition**: Accurately identifies students using the `face_recognition` library.
- 🔒 **OTP Login**: Secure authentication via email-based OTP.
- ⏱️ **Real-Time Tracking**: Logs attendance with timestamps in Excel.
- 📧 **Absentee Emails**: Notifies absent students automatically.
- 🌐 **Web Interface**: Intuitive pages for login, home, scanning, and attendance viewing.
- 🛠️ **Session Control**: Prevents duplicate attendance in a single session.

---

## 📸 Screenshots
Explore the system’s interface with the screenshots below, located in the `screenshots/` folder.

**Login Page**  
![Login Page](screenshots/Login.png)  
<br><br>

**Home Page**  
![Home Page](screenshots/home.png)  
<br><br>

**Scan & Mark**  
![Scan & Mark](screenshots/detect%20(1).png)  
<br><br>

**Attendance**  
![Attendance](screenshots/check%26mail.png)

---

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

---

## 🔧 Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Guna42/Attendance_Automation_FaceRecognition.git
   cd Attendance_Automation_FaceRecognition
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Email**:
   Update `face_recognition_live.py` with your email settings:
   ```python
   app.config['MAIL_SERVER'] = 'smtp.gmail.com'
   app.config['MAIL_PORT'] = 587
   app.config['MAIL_USE_TLS'] = True
   app.config['MAIL_USERNAME'] = "your-email@srmap.edu.in"
   app.config['MAIL_PASSWORD'] = "your-app-password"
   app.config['MAIL_DEFAULT_SENDER'] = "your-email@srmap.edu.in"
   ```

4. **Set Up Database**:
   Ensure `attendance_system.db` exists and includes a `teachers` table with an `email` column.

5. **Prepare Known Faces**:
   Add student images to the `known_faces/` directory and update `known_faces_db` in the code.

6. **Run the Application**:
   ```bash
   python face_recognition_live.py
   ```

7. Access at `http://127.0.0.1:5000`.

---

## 🚀 Usage
- **Login**: Visit `/`, enter your email, and verify the OTP.
- **Home**: Go to `/Home` to select "Check Attendance" or "Scan & Mark".
- **Scan & Mark**: At `/scan`, click "Start" to scan faces, then "Stop" to finish.
- **View Attendance**: Check `/attendance` to review logs and send absentee emails.
- **Logout**: Close the browser to end the session.

---

## 📂 File Structure
- `face_recognition_live.py`: Core Flask application.
- `templates/`: HTML templates for the web interface.
- `static/`: CSS, JavaScript, and static images.
- `screenshots/`: Screenshot images for documentation.
- `known_faces/`: Student images for face recognition.
- `attendance.xlsx`: Attendance logs.
- `present_students.xlsx`: List of present students.
- `absent_students.xlsx`: List of absent students.
- `attendance_system.db`: SQLite database.

---

## 📝 Notes
- Ensure your webcam is connected and functional.
- Adjust `process_every_n_frames` in the code for optimal performance.
- Attendance files are reset on application startup.
- Fine-tune the face recognition threshold and margin as needed.

---

## 🤝 Contributing
Want to improve the project? Fork the repository, make your changes, and submit a pull request!

---

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 🙌 Acknowledgments
- Powered by the `face_recognition` library.
- Built with Flask and SQLite.
- Developed at SRM University AP.

---