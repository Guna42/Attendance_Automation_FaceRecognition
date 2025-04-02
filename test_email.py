import smtplib

email = "yashwanth_seeram@srmap.edu.in"
password = "cabr ymzw meda lrud"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    print("Login worked! Credentials are good.")
    server.quit()
except Exception as e:
    print(f"Error: {e}")