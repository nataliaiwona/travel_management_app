"""Travel Management Application"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, PinType, Location, Pin 

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar 
app.secret_key = "MEMORY"

# Raises and error for when you use an undefined variable in Jinja2. 
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page."""

    return render_template("landing_page.html")


@app.route('/signup', methods=['GET'])
def signup_form():
    """Show form for user signup."""

    return render_template("signup_form.html")


@app.route('/signup', methods=['POST'])
def signup_process():
    """Process signup."""

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash("Thanks for signing up, {}! Bon Voyage!".format(fname))
    return redirect("/user_homepage/{}".format(new_user.id))


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
   # return redirect("/TKTK/{}".format(user.id))

@app.route('/logout')
def logout():
    """Log out."""

    del session["id"]
    flash("You are now logged Out.")
    return redirect("/")


#@app.route('/user_homepage/<int:user_id')
def user_homepage():
    """Show user's map."""

    user = User.query.get(user_id)
    return 









if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the point
    # of invoking the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()