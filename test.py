from flask import Flask, flash, redirect, render_template, request, session
import json 
import sqlite3
import time
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from functools import wraps
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)





def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/landing")
        return f(*args, **kwargs)

    return decorated_function

@login_required
def get_username():
    userid = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print(userid)
    cur.execute("SELECT username FROM users WHERE id = ?", (userid,));
    row = cur.fetchone()
    username = row["username"]
    cur.close()
    conn.close()
    return username

@login_required
def get_email():
    userid = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT email FROM users WHERE id = ?", (userid,));
    row = cur.fetchone()
    email = row["email"]
    cur.close()
    conn.close()
    return email


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if request.form.get("username"):
            if request.form.get("password"):
                username = request.form.get("username")
                password = request.form.get("password")
                conn = sqlite3.connect("data.db")
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE username = ?", (username,))
                row = cur.fetchone()
                cur.close()
                conn.close()
                if row is None or not check_password_hash(row[3], password):
                    flash("Invalid username and/or password")
                    return redirect("/login")
                session["user_id"] = row[0]
                return redirect("/")
                
    else:
        return render_template("login.html")

@app.route("/")
@login_required
def home():
    username = get_username()
    user_id = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM birds WHERE flock_id IN (SELECT id FROM flocks WHERE user_id = ?)", (user_id,))
    chickens = cur.fetchall()
    return render_template("index.html", name=username, chickens=chickens)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/deletechicken", methods=["GET", "POST"])
@login_required
def deletechicken():
    chicken_id = request.args.get("id", type=int)
    user_id = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM birds WHERE flock_id IN (SELECT id FROM flocks WHERE user_id = ?) AND id = ?", (user_id, chicken_id))
    chickens = cur.fetchone()
    if request.method == "POST":
        cur.execute("DELETE FROM birds WHERE id = ?", (chicken_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect("/flock")
    else:
        
        cur.close()
        conn.close()
        return render_template("deletechicken.html", chicken=chickens)
    pass

@app.route("/editchicken", methods=["GET", "POST"])
@login_required
def editchicken():
    chicken_id = request.args.get("id", type=int)
    print(chicken_id)
    user_id = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM birds WHERE flock_id IN (SELECT id FROM flocks WHERE user_id = ?) AND id = ?", (user_id, chicken_id))
    chickens = cur.fetchone()
    if request.method == "POST":
        if request.form.get("name"):
            if request.form.get("breed"):
                if request.form.get("birth"):
                    chicken_name = request.form.get("name")
                    chicken_breed = request.form.get("breed")
                    chicken_birth = request.form.get("birth")   
                    chicken_info = request.form.get("info")
                    chicken_id = request.args.get("id", type=int)
                    print(chicken_id)
                    cur.execute("UPDATE birds SET name = ?, breed = ?, birth_date = ?, info = ? WHERE id = ?", (chicken_name, chicken_breed, chicken_birth, chicken_info, chicken_id))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print("Updated chicken info")
                    return redirect("/flock")
                else:
                    return render_template("chickenerror.html", logerror="No chicken birthday entered")

            else:
                return render_template("chickenerror.html", logerror="No chicken breed entered")
        else:
            return render_template("chickenerror.html", logerror="No chicken name entered")



    else:
        cur.close()
        conn.close()
        
        return render_template("editchicken.html", chicken=chickens)

@app.route("/error_page")
def error_page():
    return render_template("error_page.html")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    
    if request.method == "POST":
        if request.form.get("username"):
            if request.form.get("password"):
                if request.form.get("email"):

                    username = request.form.get("username")
                    password = request.form.get("password")
                    email = request.form.get("email")
                    print("Successfully received data")
                    


                    password = generate_password_hash(password)
                    conn = sqlite3.connect("data.db")
                    cur = conn.cursor()
                    conn.row_factory = sqlite3.Row
                    cur.execute("SELECT * FROM users WHERE username = ?", (username,)); 
                    if cur.fetchone() is not None:
                        return render_template("login_error.html", logerror="Username taken")
                    cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
                    conn.commit()
                    cur.execute("SELECT id FROM users WHERE username = ?", (username,));
                    tmp = cur.fetchone()
                    id = tmp[0]
                   
                    session["user_id"] = id;
                                      
                    cur.close()
                    conn.close()
                    return redirect("/")
                else:
                    return render_template("login_error.html", logerror="No email")
            else:
                return render_template("login_error.html", logerror="No password")
        else:
            return render_template("login_error.html", logerror="No username")
    # Make apology page if it fails to insert data
    else:
        return render_template("signup.html")

@app.route("/stats")
@login_required
def chickens():
    return render_template("stats.html")

@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/signin", methods=["GET", "POST"] )
def signin():
    if request.method == "POST":
        if request.form.get("username"):
            if request.form.get("password"):
                username = request.form.get("username")
                password = request.form.get("password")
                print("Successfully received data")

                conn = sqlite3.connect("data.db")
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE username = ?", (username,));
                row = cur.fetchone()
                

                cur.close()
                conn.close()
                if row is None:
                    flash("Invalid username and/or password")
                    return redirect("/signin")
                tmp = row["password"]
                print(tmp)
                if check_password_hash(tmp, password):
                    session["user_id"] = row["id"]
                    return redirect("/")
                else:
                    
                    return render_template("login_error.html", logerror="Username/password incorrect")
            else:
                return render_template("login_error.html", logerror="No password")
        else:
            return render_template("login_error.html", logerror="No username")
    else:
       return render_template("signin.html")


@app.route("/user")
@login_required
def user():
    username = get_username()
    email = get_email()
    return render_template("user.html", email=email, username=username )


@app.route("/addchicken", methods=["GET", "POST"])
@login_required
def addchicken():
    if request.method == "POST":
        if request.form.get("name"):
            if request.form.get("breed"):
                if request.form.get("birth"):
                    chicken_name = request.form.get("name")
                    chicken_breed = request.form.get("breed")
                    chicken_birth = request.form.get("birth")
                    print(chicken_breed)
                    user_id = session["user_id"]
                    conn = sqlite3.connect("data.db")
                    conn.row_factory = sqlite3.Row
                    cur = conn.cursor()
                    cur.execute("SELECT id FROM flocks WHERE user_id = ?", (user_id,))
                    flock_id = cur.fetchall()
                    if flock_id is None:
                        print("No flock found, creating new flock")
                        cur.execute("INSERT INTO flocks (user_id) VALUES (?)", (user_id,))
                        conn.commit()
                        cur.execute("SELECT id FROM flocks WHERE user_id = ?", (user_id,))
                        flock_id = cur.fetchall()
                    if request.form.get("info"):
                        chicken_info = request.form.get("info")
                        cur.execute("INSERT INTO birds (flock_id, name, breed, birth_date, info) VALUES (?, ?, ?, ?, ?)", (flock_id[0]["id"], chicken_name, chicken_breed, chicken_birth, chicken_info))
                        conn.commit()
                    else:
                        cur.execute("INSERT INTO birds (flock_id, name, breed, birth_date) VALUES (?, ?, ?, ?)", (flock_id[0]["id"], chicken_name, chicken_breed, chicken_birth))
                        conn.commit()
                    cur.close()
                    conn.close()
                    return redirect("/flock")
                else:
                    return render_template("chickenerror.html", logerror="No chicken birthday entered")
            else:
                return render_template("chickenerror.html", logerror="No chicken breed entered")
        else:
            return render_template("chickenerror.html", logerror="No chicken name entered")
    else:
        return render_template("add_chicken.html")

@login_required
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/landing")

@login_required
@app.route("/flock")
def flock():
    user_id = session["user_id"]
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id FROM flocks WHERE user_id = ?", (user_id,))
    flock_id = cur.fetchall()
    if flock_id is None:
        
        return redirect("/addchicken")
    cur.execute("SELECT * FROM birds WHERE flock_id = ?", (flock_id[0]["id"],))
    birds = cur.fetchall()
    
    cur.close()
    conn.close()
    user_name = get_username()
    return render_template("flock.html", chickens=birds, name=user_name)


if __name__ == '__main__':
  print("THIS IS THE TEST APP")
  try:
    app.run(debug=True, port=8000)
    print("Flask app ended")
  except Exception as e:
    print(f"An error occurred: {e}")