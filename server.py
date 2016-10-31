"""Travel Management Application"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, PinType, Location, Pin 

a = Flask(__name__)

# Required to use Flask sessions and the debug toolbar 
app.secret_key = "MEMORY"

# Raises and error for when you use an undefined variable in Jinja2. 
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")

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