from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
<<<<<<< HEAD
=======
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_assets import Bundle, Environment
import tkinter

>>>>>>> 4a6e9706440a465af920f0194ccb10cc7ee51d0f

app = Flask(__name__)

@app.route("/")
def index():
<<<<<<< HEAD
    return render_template("home.html")
=======
    return render_template("test.py")
>>>>>>> 4a6e9706440a465af920f0194ccb10cc7ee51d0f

if __name__ == "__main__":
    app.run(debug = True)
