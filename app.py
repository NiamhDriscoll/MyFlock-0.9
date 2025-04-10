from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")
@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/signup")
def signup():
    return render_template("sign_up.html")

if __name__ == '__main__':
  print("Flask app started")
  try:
    app.run(debug=True)
    print("Flask app ended")
  except Exception as e:
    print(f"An error occurred: {e}")