import sqlite

def init_db():
    conn = sqlite3.connect("C:\\Users\\Niamh\\OneDrive\\Desktop\\MyFlock 0.6\\myflock.db")
    cur = conn.cursor()
    cur.execute (''' CREATE TABLE IF NOT EXISTS people
(username TEXT, email TEXT, password TEXT)''')


def insert(username, email, password):
    try: 
        conn = sqlite3.connect("C:\\Users\\Niamh\\OneDrive\\Desktop\\MyFlock 0.6\\myflock.db")
        cur = conn.cursor
        cur.execute("INSERT INTO people (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
    finally:
     if cur:
        cur.close()
     if conn:
        conn.close 

