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
app.jinja_env.auto_reload = True


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
    return redirect("/user_homepage")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html", loggingin=True)


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

    session["user_id"] = user.id

    flash("Logged in!")
    return redirect("/user_homepage")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You are now logged out.")
    return redirect("/")


@app.route('/user_homepage')
def user_homepage():
    """Show logged-in user's map."""

    print "User Homepage"

    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
        # need to access user object    
        # query for user info - aka existing pins
    else:
        flash("Please log in to see your map.")
        return redirect("/login")

    return render_template("user_homepage.html")

@app.route('/add_pins')
def add_pins():
    """Allow user to add pins to map!"""

    print "Add Pins to Map"

    user_id = session.get("user_id")

    if user_id:
        user=User.query.get(user_id)
    else:
        flash("Please log in to add pins to your map.")
        return redirect("/login")

    return render_template("add_pins.html")




if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the point
    # of invoking the DebugToolbarExtension

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
