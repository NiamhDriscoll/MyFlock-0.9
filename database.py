import sqlite3
import json

with open("data.json", "r") as f:
    data = json.load(f)
    for username in data:["username"]
    for password in data:["password"]
    for email in data:["email"]
    

  
# Remove when ready to use database
def init_db():
    conn = sqlite3.connect("/home/nolson/data/data.db")
    cur = conn.cursor()
    cur.execute (''' CREATE TABLE IF NOT EXISTS people
(username TEXT, email TEXT, password TEXT)''')


def insert(username, email, password):
    try: 
        conn = sqlite3.connect("/home/nolson/data/data.db")
        cur = conn.cursor
        cur.execute("INSERT INTO people (username TEXT, email TEXT, password TEXT) VALUES (?, ?, ?)", (username, email, password))
        print("Data inserted successfully")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    else:
        conn.commit()
    finally:
     if cur:
        cur.close()
     if conn:
        conn.close 

