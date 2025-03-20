import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database (creates it if it doesn’t exist)
conn = sqlite3.connect('parking.db')
cursor = conn.cursor()

# Create users table with role
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  is_admin BOOLEAN DEFAULT 0
                  )''')

# Create parking_spots table with user_id
cursor.execute('''CREATE TABLE IF NOT EXISTS parking_spots (
                  spot_id INTEGER PRIMARY KEY,
                  status TEXT NOT NULL,
                  user_plate TEXT,
                  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                  latitude REAL,
                  longitude REAL,
                  user_id INTEGER DEFAULT NULL,
                  FOREIGN KEY (user_id) REFERENCES users(user_id)
                  )''')

# Create reservations table with user_id
cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                  reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  spot_id INTEGER,
                  user_id INTEGER NOT NULL,
                  start_time DATETIME NOT NULL,
                  end_time DATETIME NOT NULL,
                  FOREIGN KEY (spot_id) REFERENCES parking_spots(spot_id),
                  FOREIGN KEY (user_id) REFERENCES users(user_id)
                  )''')

# Clear existing users and insert only admin
cursor.execute("DELETE FROM users")
cursor.execute("INSERT INTO users (user_id, username, password_hash, is_admin) VALUES (?, ?, ?, ?)", 
               (1, 'admin', generate_password_hash('sliot'), 1))  # Admin user, user_id = 1

# Insert 20 sample spots with placeholder coordinates and no user_id (available)
# Example coordinates for a parking lot: 37.4419, -122.1430 (Palo Alto area)
spots = [
    (i, 'available', None, None, 37.4419 + (i * 0.0001), -122.1430 + (i * 0.0001), None)
    for i in range(1, 21)
]
cursor.executemany("INSERT OR IGNORE INTO parking_spots (spot_id, status, user_plate, last_updated, latitude, longitude, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", spots)

# Save changes and close
conn.commit()
conn.close()

print("Database initialized with admin (user_id=1) and 20 parking spots.")