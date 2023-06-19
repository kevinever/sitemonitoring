import psycopg2
from datetime import datetime, timedelta

# Establish connection to database
conn = psycopg2.connect(dbname='monitoring', user='postgres', password='post123', host='localhost')

# Create tables
def create_table():
    """Create the urls and defaced_websites tables if they don't exist."""
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS defaced_websites (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            defaced_time TIMESTAMP NOT NULL DEFAULT NOW(),
            content_before TEXT NOT NULL,
            content_after TEXT NOT NULL
        )
    """)
    cur.execute(""" 
    CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);

    """)
    cur.execute(""" 
    INSERT INTO users (email) VALUES ('kalisadoe@gmail.com'), ('example2@example.com');

    """)
    conn.commit()


# Insert dummy data into urls table
def insert_urls():
    """Insert dummy data into urls table."""
    cur = conn.cursor()
    cur.execute("INSERT INTO urls (url, status) VALUES ('http://www.example.com', 'active')")
    cur.execute("INSERT INTO urls (url, status) VALUES ('http://www.google.com', 'inactive')")
    cur.execute("INSERT INTO urls (url, status) VALUES ('http://www.facebook.com', 'active')")
    conn.commit()

# Insert dummy data into defaced_websites table
def insert_defaced_websites():
    """Insert dummy data into defaced_websites table."""
    cur = conn.cursor()
    url1 = "http://www.example.com"
    url2 = "http://www.google.com"
    url3 = "http://www.facebook.com"
    now = datetime.now()
    before1 = "This is the content of example.com before it was defaced."
    after1 = "This is the content of example.com after it was defaced."
    before2 = "This is the content of google.com before it was defaced."
    after2 = "This is the content of google.com after it was defaced."
    before3 = "This is the content of facebook.com before it was defaced."
    after3 = "This is the content of facebook.com after it was defaced."
    cur.execute("INSERT INTO defaced_websites (url, defaced_time, content_before, content_after) VALUES (%s, %s, %s, %s)", (url1, now - timedelta(days=1), before1, after1))
    cur.execute("INSERT INTO defaced_websites (url, defaced_time, content_before, content_after) VALUES (%s, %s, %s, %s)", (url2, now - timedelta(hours=6), before2, after2))
    cur.execute("INSERT INTO defaced_websites (url, defaced_time, content_before, content_after) VALUES (%s, %s, %s, %s)", (url3, now - timedelta(minutes=30), before3, after3))
    conn.commit()



# Call functions to create and insert data into tables
create_table()
insert_urls()
insert_defaced_websites()
