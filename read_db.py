import sqlite3

# Connect to the database (replace 'your_database.db' with your database name)
conn = sqlite3.connect('turnstile.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute a query to select data from your table
cursor.execute('SELECT * FROM TurnstileData')

# Fetch the results
rows = cursor.fetchall()

# Process the fetched data
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
