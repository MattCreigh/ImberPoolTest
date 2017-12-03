from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_assets import Bundle, Environment
import tkinter


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("test.py")

if __name__ == "__main__":
    app.run(debug = True)
