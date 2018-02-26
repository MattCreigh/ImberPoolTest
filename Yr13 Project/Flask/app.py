
### IMPORTS ################################################################################

from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, PasswordField, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from testLib import *


### APP-CONFIG ###############################################################################

app = Flask(__name__)
mysql = MySQL(app)


### MySQL-CONFIG ############################################################################

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "H1nchley"
app.config["MYSQL_DB"] = "schema2"
app.config["MYSQL_HOST"] = "localhost"

### SECRET KEY #############################################################################

app.secret_key = "6d61374da4b4df53c6f8fbf4c9b05576d647a07da7498b400abaf7e1f4f44124"

### LOGIN ROUTE ############################################################################

@app.route("/", methods=["GET","POST"])

def login():

    try :
        if session["logged"] == True:
            return redirect(url_for("profile"))
        else:
            session["logged"] == False
    except:
        form = LogInForm(request.form)

        if request.method == "POST" and form.validate():
            try:
                cur = mysql.connection.cursor()
                cur.execute("""SELECT * FROM trunk_user_index WHERE userName = "%s";""" %str(form.UserName.data))
                userIndex = cur.fetchone()
                cur.close()
                log("password", (userIndex)[2])
                if sha256_crypt.verify(form.Password.data, (userIndex[2])):
                    session["logged"] = True
                    session["username"] = form.UserName.data
                    session["userID"] = cur.fetchmany(0)
                    return redirect(url_for("profile"))
                else:
                    flash(" Incorrect username or password!!!")
                    return redirect(url_for("login"))
            except:
                flash(" Incorrect username or password!!!")
                return redirect(url_for("login",))
        return render_template("login.html", form=form)

class LogInForm(Form):
    UserName = StringField(u"UserName", validators = [validators.input_required(message="You forgot to enter your Username!") ,
    validators.Length(min = 4, max=20, message="Usernames are between 4 and 20 characters long")])

    Password = PasswordField(u"Password", validators = [validators.input_required(message="You forgot to enter your password!"),
    validators.Length(min=5, max=20, message="Usernames are between 4 and 20 characters long")])



### PROFILE ROUTE ##########################################################################

@app.route("/profile", methods=["GET", "POST"])

def profile():
    tableList = []
    shiftDays = []
    tableRowList = []
    dayShiftList = []
    shiftCount = int()

    def tableRow(day,startTime, finishTime):
        tableRowList = [day, startTime, finishTime]
        tableList.append(tableRowList)
        return tableList


    if "logged" in session:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM trunk_user_index WHERE userName = "%s";""" % session["username"])
        userInfoList = cur.fetchone()
        cur.close()

        if session["username"] == "admin":
            return redirect(url_for("adminProfile"))

        else:
            for n in range(3, len(userInfoList)):
                if userInfoList[n] == "y":
                    shiftDays.append(cur.description[n][0])
                    shiftCount = len(shiftDays)

            for n in range(0, shiftCount):
                cur = mysql.connection.cursor()
                cur.execute("""SELECT * FROM %s WHERE %s = "%s";""" % (shiftDays[n], (shiftDays[n][0:3])+"UserID", userInfoList[0]))
                try:
                    dayShiftList = cur.fetchall()[0]
                    cur.close()
                    day = shiftDays[n]
                    startTime = str(dayShiftList[2])
                    finishTime = str(dayShiftList[3])
                    tableRow(day,startTime,finishTime)
                except:
                    cur.close()
                    continue

        return render_template("profile.html",
                               shiftCount = shiftCount,
                               userInfoList = userInfoList,
                               shiftDays = shiftDays,
                               tableList = tableList)

    else:
        return redirect(url_for("login"))


### ADMIN PROFILE ROUTE ####################################################################

@app.route("/adminprofile", methods=["GET", "POST"])

def adminProfile():
    tableList = []
    dayShiftList = []
    shiftDays = []
    shiftCount = 0

    def adminTableRow(day,name,startTime,finishTime):
        adminTableRowList = [day, name, startTime, finishTime]
        tableList.append(adminTableRowList)
        return tableList

    shiftDays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM trunk_user_index""")
    stage1 = cur.fetchall()
    for n in range(0, len(stage1)):
        stage2 = stage1[n]
        for n in range(3, len(stage2)):
            if stage2[n] == "y":
                shiftCount = shiftCount+1

    for n in range(0, 7):
        day = shiftDays[n]
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM %s;""" % (shiftDays[n]))
        dayShiftList = cur.fetchall()
        cur.close()
        for n in range(0, len(dayShiftList)):
            startTime = str(dayShiftList[n][2])
            finishTime = str(dayShiftList[n][3])
            try:
                cur = mysql.connection.cursor()
                cur.execute("""SELECT * FROM trunk_user_index WHERE userID = %s;""" %dayShiftList[n][1])
                name = cur.fetchone()[1]
                cur.close()
            except:
                continue
            adminTableRow(day, name, startTime, finishTime)

        shiftCount = len(tableList)
    return render_template("adminProfile.html",
                           shiftCount = shiftCount,
                           shiftDays = shiftDays,
                           tableList = tableList)


### LOGOUT ROUTE ###########################################################################

@app.route("/logout", methods=["GET", "POST"])

def logOut():
    if "logged" in session:
        session.pop("logged")
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
