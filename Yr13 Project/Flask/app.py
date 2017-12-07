from flask import Flask, render_template, flash, redirect, url_for, session, logging, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug = True)
