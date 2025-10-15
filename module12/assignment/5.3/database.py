import sqlite3 
 
def setup_database(): 
    conn = sqlite3.connect('events.db') 
    c = conn.cursor() 
     
    c.execute(''' 
        CREATE TABLE IF NOT EXISTS events ( 
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            type TEXT,  -- 'indoor' or 'outdoor' 
            description TEXT, 
            location TEXT, 
            date TEXT,
            time TEXT 
        ) 
    ''') 
     
    # Sample events 
    events = [ 
        ('Summer Concert', 'outdoor', 'Live music in the park', 'Central Park', '2025-10-16', '18:00'), 
        ('Art Exhibition', 'indoor', 'Modern art showcase', 'City Gallery', '2025-10-16', '10:00'), 
        ('Food Festival', 'outdoor', 'International cuisine', 'Waterfront', '2025-10-16', '12:00'), 
        ('Theater Show', 'indoor', 'Classical drama', 'Grand Theater', '2025-10-16', '20:00'),
        ('Tech Conference', 'indoor', 'Latest in tech', 'Convention Center', '2025-10-17', '09:00'), 
        ('Farmers Market', 'outdoor', 'Local produce and crafts', 'Downtown Square', '2025-10-17', '08:00'),
        ('Outdoor Yoga', 'outdoor', 'Morning yoga session', 'Riverside Park', '2025-10-20', '10:00'), 
        ('Book Fair', 'indoor', 'Books from various genres', 'Community Center', '2025-10-18', '11:00'),
        ('Charity Run', 'outdoor', '5K run for a cause', 'City Stadium', '2025-10-18', '06:00'),
        ('Cooking Workshop', 'indoor', 'Learn to cook Italian cuisine', 'Culinary School', '2025-10-19', '14:00')
    ] 
     
    c.executemany('INSERT OR IGNORE INTO events (name, type, description, location, date, time) VALUES (?,?,?,?,?,?)', events) 
    conn.commit() 
    conn.close() 
 
if __name__ == "__main__": 
    setup_database()