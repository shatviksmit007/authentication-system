import sqlite3
import random

# Connect to the database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Turn off foreign key constraints and begin a transaction
cursor.execute("PRAGMA foreign_keys=off")
cursor.execute("BEGIN TRANSACTION")

# Add a new column "passcode" to the table
# cursor.execute("ALTER TABLE students ADD COLUMN passcode TEXT")

# Generate and update a unique passcode for each user
cursor.execute("SELECT admission_number FROM students")
users = cursor.fetchall()
for user in users:
    passcode = ''.join(random.choice('0123456789') for i in range(6))
    cursor.execute("UPDATE students SET passcode = ? WHERE admission_number = ?",
                   (passcode, user[0]))

# Commit the transaction and turn on foreign key constraints
cursor.execute("COMMIT")
cursor.execute("PRAGMA foreign_keys=on")

# Commit the changes and close the connection
conn.commit()
conn.close()
