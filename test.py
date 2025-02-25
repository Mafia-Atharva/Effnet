import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Query all users from the 'users' table
c.execute("SELECT * FROM users")

# Fetch all results
users = c.fetchall()

# Fetch column names for better display
columns = [description[0] for description in c.description]

# Display column names and all entries
if users:
    print(" | ".join(columns))  # Display column names
    print("-" * 100)  # Separator line
    for user in users:
        print(" | ".join(map(str, user)))  # Display each user's data
else:
    print("No users found.")

# Close the connection
conn.close()
