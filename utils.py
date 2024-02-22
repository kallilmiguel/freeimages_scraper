import sqlite3
import uuid
from datetime import datetime

def insert_image_url(db_path, url):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    date = datetime.now()

    c.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, createdAt TIMESTAMP)")
    
    c.execute("INSERT OR IGNORE INTO images (url, createdAt) VALUES (?, ?)", 
              (url, date))
    conn.commit()
    conn.close()