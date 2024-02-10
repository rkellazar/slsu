import sqlite3


def create_table2():
    # Connect to SQLite database
    conn = sqlite3.connect('turnstile.db')  # Replace with your database name
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='TimelogData'")
    table2_exists = cursor.fetchone()

    # Create the second table if it doesn't exist
    if not table2_exists:
        cursor.execute('''CREATE TABLE TimelogData (
                           id TEXT,
                           login_time DATETIME,
                           inout TEXT
                           )''')
        
    # Commit changes and close connection
    conn.commit()
    conn.close()