import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect("attendance_system.db")
cursor = conn.cursor()

# Create the teachers table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL
    );
""")

# List of teacher emails to insert
teacher_emails = [
    ("yashwanth_seeram@srmap.edu.in",),
    ("gunavardhan_byraju@srmap.edu.in",),
    ("kartheek_sanka@srmap.edu.in",),
    ("saisumanth_oruganti@srmap.edu.in",)
]

# Insert teacher emails (IGNORE prevents duplicates)
cursor.executemany("INSERT OR IGNORE INTO teachers (email) VALUES (?);", teacher_emails)

# Commit and close
conn.commit()
conn.close()

print("Database setup complete. Teachers table created successfully!")
