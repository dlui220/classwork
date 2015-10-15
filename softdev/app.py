from flask import Flask, render_template, session, redirect, url_for, request, flash, Markup
import util

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", session=session)

@app.route("/about")
def about():
    return render_template("about.html", session=session)

@app.route("/story")
def story():
#generates html for displaying the title as a link
    str=""
    stories=util.getAllPosts()
    for item in stories:
        str+='"<div class="col-md-offset-2 col-md-8 row">'
        str+='<h2 class="text-primary">%s</h3>' %(item[1])
        str+="<blockquote>"
        str+='<p class="text-muted">%s</p>' %(item[2])
        str+='<footer class="text-info"> %s </footer>' %(item[0])
        str+="</blockquote>"
        str+='</div>'

    str = Markup(str)

    return render_template("story.html", allposts=str)
   # return render_template("story.html")

@app.route("/login", methods = ["GET"])
def login():
    
    return render_template("login.html")

@app.route("/login", methods = ["POST"])
def login2():
    user = request.form['username']
    password = request.form['password']
    button = request.form['button']

    if util.authenticate(user,password):
        session['username'] = user
        flash("you were successfully logged in")
        return redirect(url_for("home"))
    flash("invalid username or password")
    return render_template("login.html", session=session)
    

@app.route("/newpost", methods=['GET','POST'])
def newpost():
    if request.method=="GET":
        return render_template("newpost.html")
    else:
        uname=session['username']
        button=request.form['button']
        title=request.form['nTitle']
        content=request.form['nContent']
        if button=="Post":
            util.makePost(uname,title,content)
            return redirect(url_for('story'))
        if button=="cancel":
            return redirect(url_for('home'))
        return render_template('newpost.html', session=session)


@app.route("/reset")
@app.route("/logout")
def reset():
    #works whether or not 'username' is in session
    session.pop('username', None);
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.debug = True
    app.secret_key="secret"
    app.run(host = "0.0.0.0", port = 8000)
