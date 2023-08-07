from flask import Flask, render_template
app=Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

app.run(debug=True)