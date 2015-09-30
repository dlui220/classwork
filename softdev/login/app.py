from flask import Flask, render_template, request, session
from flask import redirect, url_for
import utils

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("about.html")

@app.route("/reset")
def reset():
    session['n'] = False
    return redirect(url_for('login'))

@app.route("/secret")
def secret():
    if session['n'] == False:
        return "<h1>Error: Not logged in.</h1>"
    else:
        return render_template("secret.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        if 'n' not in session:
            session['n'] = False
        uname = request.form['username']
        pword = request.form['password']
        button = request.form['button']
        if button == "cancel":
            return render_template('login.html')

        if utils.authenticate(uname,pword):
            session['n'] = True
            return render_template("success.html")
        else:
            session['n'] = False
            error="Invalid user or password"
            return render_template("login.html",err=error)
        

if __name__ == "__main__":
   app.debug = True
   app.secret_key="Don't store this on github"
   app.run(host="0.0.0.0", port=8000)
