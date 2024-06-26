import sqlite3
import os
from datetime import datetime

def fetch_and_display_data():
    # Connect to the SQLite database
    database_path = os.path.join(os.path.dirname(__file__), '..',
    'nanoswai.db')
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Execute SQL query to select all records from the table
    cursor.execute('select id, start_time, end_time, duration, power, priority_t, priority_e from camera_computer limit 100')

    # Fetch and display the results
    results = cursor.fetchall()

    # Format and display data in a readable table format
    print("ID  | Start Time (UTC)    | End Time (UTC)      | Duration (s) | Power (W) | Priority T  | Priority E")
    print("-" * 104)  # Print a divider line for clarity

    for row in results:
        start_time_formatted = datetime.utcfromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')
        end_time_formatted = datetime.utcfromtimestamp(row[2]).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{row[0]:<3} | {start_time_formatted} | {end_time_formatted} | {row[3]:<12} | {row[4]:<9.2f} | {row[5]:<10.2f} | {row[6]:<10.2f}")

    # Close the database connection
    conn.close()

# Call the function to display the data
fetch_and_display_data()

