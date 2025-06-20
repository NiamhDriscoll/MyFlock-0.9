from flask import Flask, render_template, redirect, url_for, request
import json 
import sqlite3

app = Flask(__name__)




def insert(username, email, password):
    try:
        conn = sqlite3.connect("/home/nolson/data/data.db")
        cur = conn.cursor()
        cur.execute (''' CREATE TABLE IF NOT EXISTS people
(username TEXT, email TEXT, password TEXT)''')
        with open("data.json", "r") as f:
         data = json.load(f)
         username = data["username"]
         password = data["password"]
         email = data["email"]
         cur.execute("INSERT INTO people (username, email, password) VALUES (?, ?, ?)", (username, email, password))
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



@app.route("/")
def home():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        print("Successfully received data")
        
        new_user = {
        "username": username,
        "password": password,
        "email" : email
        }
        with open("data.json", "w") as f:
         json.dump(new_user, f, indent=4)
        print("Data saved to data.json")
        try:
         insert(username, email, password)
         print("User data added to database")
        except sqlite3.Error as e:
            print(f"An error occurred while inserting data: {e}")
            return redirect(url_for("home"))
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
            return redirect(url_for("home"))
    # Make apology page if it fails to insert data

    return render_template("sign_up.html")
@app.route("/chickens")
def chickens():
    return render_template("chickens.html")

if __name__ == '__main__':
  print("Flask app started")
  try:
    app.run(debug=True, port=8000)
    print("Flask app ended")
  except Exception as e:
    print(f"An error occurred: {e}")