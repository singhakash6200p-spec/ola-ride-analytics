import pandas as pd
import sqlite3

# CSV padhein
df = pd.read_csv('Bookings.csv')

# SQLite database se connect karein
conn = sqlite3.connect('ola_rides.db')

# Data ko SQL table mein daalein
df.to_sql('rides', conn, if_exists='replace', index=False)

# Check karein
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM rides")
print(f"Total rows loaded: {cursor.fetchone()[0]}")

conn.close()
