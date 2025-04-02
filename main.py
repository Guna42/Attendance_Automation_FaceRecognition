import pandas
import smtplib
import datetime
import time 
import os  # Added this import

# File path
ABSENT_FILE = r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\absent_students.csv"

# Email credentials 
MY_EMAIL = "srmap999@gmail.com"
PASSWORD = "fblq qwax wtci aijl"  

def send_absentee_emails():
    print("Starting send_absentee_emails function")
    
    # Check if file exists
    if not os.path.exists(ABSENT_FILE):
        print(f"Error: {ABSENT_FILE} not found")
        raise FileNotFoundError(f"{ABSENT_FILE} not found")

    # Read CSV file
    try:
        df = pandas.read_csv(ABSENT_FILE)
        print(f"Loaded {ABSENT_FILE} with {len(df)} rows")
    except Exception as e:
        print(f"Error reading {ABSENT_FILE}: {e}")
        raise

    if df.empty:
        print("No absentees found in CSV")
        return  # No emails to send, but not an error

    # Get date and time
    today = datetime.datetime.now()
    today_date = today.strftime("%Y-%m-%d")  
    current_time = today.strftime("%H:%M:%S")  

    for index, row in df.iterrows():
        if row["Status"].strip().lower() == "absent":
            name = row["Name"]
            recipient_email = row["Email"]

            # Read letter template
            try:
                with open(r"C:\Users\GUNA\Videos\Recordings\Attendence_Automation\templates\letter_1.txt") as file:
                    content = file.read()
                    message = content.replace("NAME", name).replace("DATE", today_date).replace("TIME", current_time)
                print(f"Prepared email for {name} ({recipient_email})")
            except Exception as e:
                print(f"Error reading letter template: {e}")
                raise

            # Send email
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as connect:
                    connect.starttls() 
                    connect.login(MY_EMAIL, PASSWORD)
                    connect.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=recipient_email,
                        msg=f"Subject: IMPORTANT Attendance Notification\n\n{message}"
                    )
                print(f"Email successfully sent to {name} ({recipient_email})")
                time.sleep(2)  # Avoid rate limits
            except Exception as e:
                print(f"Failed to send email to {name} ({recipient_email}): {e}")
                raise  # Bubble up the error

    print("All emails processed!")

if __name__ == "__main__":
    send_absentee_emails()