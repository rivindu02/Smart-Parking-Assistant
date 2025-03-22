import sqlite3
from werkzeug.security import generate_password_hash

# Connect to SQLite database (creates it if it doesn’t exist)
conn = sqlite3.connect('parking.db')
cursor = conn.cursor()

# Create tables (unchanged)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  is_admin BOOLEAN DEFAULT 0
                  )''')

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

cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                  reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  spot_id INTEGER,
                  user_id INTEGER NOT NULL,
                  start_time DATETIME NOT NULL,
                  end_time DATETIME NOT NULL,
                  FOREIGN KEY (spot_id) REFERENCES parking_spots(spot_id),
                  FOREIGN KEY (user_id) REFERENCES users(user_id)
                  )''')

# Insert admin user
cursor.execute("INSERT OR IGNORE INTO users (user_id, username, password_hash, is_admin) VALUES (?, ?, ?, ?)", 
               (1, 'admin', generate_password_hash('sliot'), 1))

# New coordinates for a 50x40m parking lot near Palo Alto (base: 37.4419, -122.1430)
# 0.000009 ~ 1 meter in latitude, 0.000012 ~ 1 meter in longitude (approx.)
spots = [
    (1, 'available', None, None, 37.441900, -122.143000 ,None),  # Top-left corner
    (2, 'available', None, None, 37.441900, -122.142960,None),
    (3, 'available', None, None, 37.441900, -122.142920,None),
    (4, 'available', None, None, 37.441900, -122.142880,None),
    (5, 'available', None, None, 37.441900, -122.142840,None),
    (6, 'available', None, None, 37.441855, -122.143000,None),  # Second row
    (7, 'available', None, None, 37.441855, -122.142960,None),
    (8, 'available', None, None, 37.441855, -122.142920,None),
    (9, 'available', None, None, 37.441855, -122.142880,None),
    (10, 'available', None, None, 37.441855, -122.142840,None),
    (11, 'available', None, None, 37.441810, -122.143000,None),  # Third row
    (12, 'available', None, None, 37.441810, -122.142960,None),
    (13, 'available', None, None, 37.441810, -122.142920,None),
    (14, 'available', None, None, 37.441810, -122.142880,None),
    (15, 'available', None, None, 37.441810, -122.142840,None),
    (16, 'available', None, None, 37.441765, -122.143000,None),  # Fourth row
    (17, 'available', None, None, 37.441765, -122.142960,None),
    (18, 'available', None, None, 37.441765, -122.142920,None),
    (19, 'available', None, None, 37.441765, -122.142880,None),
    (20, 'available', None, None, 37.441765, -122.142840,None),
]
cursor.executemany("INSERT OR IGNORE INTO parking_spots (spot_id, status, user_plate, last_updated, latitude, longitude, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", spots)

conn.commit()
conn.close()

print("Database initialized with admin (user_id=1) and 20 parking spots with realistic coordinates.")