from flask import Flask, render_template, redirect, url_for, request
import json 
from database import init_db, insert , sqlite3

app = Flask(__name__)

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
         init_db
         insert
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
    app.run(debug=True)
    print("Flask app ended")
  except Exception as e:
    print(f"An error occurred: {e}")