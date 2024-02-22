import sqlite3
import uuid
from datetime import datetime

def insert_image_url(db_path, url):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    unique_id = str(uuid.uuid4)
    date = datetime.now()

    c.execute("CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, url TEXT UNIQUE, createdAt TIMESTAMP)")
    
    c.execute("INSERT OR IGNORE INTO images (id, url, createdAt) VALUES (?, ?, ?)", 
              (unique_id, url, date))
    conn.commit()
    conn.close()