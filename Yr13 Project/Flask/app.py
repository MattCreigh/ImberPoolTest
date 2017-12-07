from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from wtforms import Form, BooleanField, StringField, PasswordField,TextAreaField, validators
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'H1nchley'
app.config['MYSQL_DB'] = 'imberpooltest'
app.config['MYSQL_HOST'] = 'localhost'


@app.route("/", methods=["GET","POST"])

def logIn():

    form = LogInForm(request.form)

    if request.method == "POST" and form.validate():
        print(form.UserName.data, form.Password.data)
        userName = str(form.UserName.data)
        password = str(form.Password.data)

        cur = mysql.connection.cursor()
        try:
            cur.execute("""SELECT * FROM users WHERE Username = "%s";""" % userName )
            if cur.fetchone()[2] == password:
                return redirect(url_for("profile"))
            else:
                return redirect(url_for("logIn"))
                error = "Incorrect username or password!"
        except:
            return redirect(url_for("logIn"))
            error = "Incorrect username or password!"
    return render_template("home.html", form=form)

class LogInForm(Form):
    UserName = StringField( "UserName",
        [validators.input_required(message="You forgot to enter your Username!"),
        validators.Length(max=20, message="Usernames are a maximum of 20 characters long")]
    )

    Password = PasswordField( "Password",
         [validators.InputRequired(message="You forgot to enter your password!"),
         validators.Length(min=1, max=20)]
    )

@app.route("/profile", methods=["GET", "POST"])

def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug = True)
