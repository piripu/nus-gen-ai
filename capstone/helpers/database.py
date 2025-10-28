import csv, sqlite3, os, datetime, logging
from helpers import Event

logger = logging.getLogger(__name__)

def create_connection() -> sqlite3.Connection:
    return sqlite3.connect('events.db')

def seed():
    # create new database everytime for testing
    if os.path.exists('events.db'):
        logger.debug("Removing existing database for seeding.")
        os.remove('events.db')

    conn = create_connection()
    c = conn.cursor()

    logger.debug("Creating database tables.")

    # Create sample tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT, 
            date TEXT, 
            time TEXT,
            location TEXT, 
            details TEXT 
        ) 
    ''') 
    
    logger.debug("Seeding the database with sample events.")
    
    # Read data from CSV file and insert into the events table
    current_dt = datetime.datetime.now()
    
    counter = 0
    with open('./.assets/sample_events.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Adjust event dates to be relative to the current date
            dt_delta = int(row['Date']) - 1
            event_date = current_dt + datetime.timedelta(days=dt_delta)
            c.execute('''
                INSERT INTO events (name, date, time, location, details) 
                VALUES (?, ?, ?, ?, ?)
            ''', (row['Name'], event_date.strftime('%Y-%m-%d'), row['Time'], row['Location'], row['Details']))
            counter += 1
    
    logger.debug(f"Inserted {counter} events into the database.")
    
    conn.commit() 
    conn.close()

def get_events_by_date(date: str) -> list[Event]:
    conn = create_connection()

    try:
        c = conn.cursor()
        # try parse date to specific format
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        logger.debug(f"Fetching events for date: {date_obj.strftime('%Y-%m-%d')}")
        
        c.execute('SELECT name, date, time, location, details FROM events WHERE date = ?', (date_obj.strftime('%Y-%m-%d'),))
        events = c.fetchall()

        logger.debug(f"Found events: {events}")

        return [Event(*event) for event in events]
    except ValueError:
        logger.error(f"Invalid date format: {date}. Expected YYYY-MM-DD.")
        return []
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return []
    finally:
        logger.debug("Closing database connection.")
        conn.close()

