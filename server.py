"""Travel Management Application"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, PinType, Location, Pin

import os
import bcrypt

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "MEMORY"
maps_key = os.environ["GOOGLE_MAPS_API_KEY"]
# Raises an error for when you use an undefined variable in Jinja2.
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

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    new_user = User(fname=fname, lname=lname, email=email,
                    password=bcrypt.hashpw(password.encode("UTF_8"), bcrypt.gensalt()))

    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(email=email).first()

    session["user_id"] = user.id

    flash("Thanks for signing up, {}! You are now logged in. Bon Voyage!".format(fname))
    return redirect("/user_homepage")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html", loggingin=True)


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if bcrypt.hashpw(password.encode("UTF_8"),
                     user.password.encode("UTF_8")).decode() == user.password:
        flash("Password matches")
    else:
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

@app.route('/user_homepage', methods=['GET'])
def show_add_pins():
    """Show page to add pins to map."""

    return render_template("user_homepage.html", api_key=maps_key)

@app.route('/user_homepage', methods=['POST'])
def user_homepage():
    """Show logged-in user's map and add pins to map."""

    print "User Homepage"

    user_id = session.get("user_id")
    print user_id

    if user_id:
        user = User.query.get(user_id)
        print user.fname
        # need to access user object
        # query for user info - aka existing pins
        # save new pins to db for specific user
    else:
        flash("Please log in to add pins to your map.")
        return redirect("/login")

    pin_type = request.form.get("pinType")
    city = request.form.get("city")
    state = request.form.get("state") if request.form.get("state") != '' else None
    country = request.form.get("country")
    lat = request.form.get("lat")
    lng = request.form.get("lng")
    location = Location.query.filter(Location.city == city,
                                     Location.country == country,
                                     Location.name == city,
                                     Location.latitude == lat,
                                     Location.longitude == lng).first()
    print pin_type, city, state, country, location

    if location is None:
        location = Location(city=city, state=state, country=country, name=city,
                            latitude=lat, longitude=lng)
        db.session.add(location)
        db.session.commit()
        print location

    print location
    new_pin = Pin(user_id=user.id,
                  pin_type_id=pin_type, location_id=location.id)

    db.session.add(new_pin)
    db.session.commit()

    print new_pin

    return "City has been added to your  map!"


@app.route('/user_pin_info.json')
def pin_info():
    """JSON information about user map pins."""
    # print Pin.query.all()

    pins = {
        pin.id: {
            "pinId": pin.id,
            "pinTypeId": pin.pin_type_id,
            "userId": pin.user_id,
            "locationId": pin.location_id,
            "city": pin.location.city,
            "state": pin.location.state,
            "country": pin.location.country,
            "latitude": pin.location.latitude,
            "longitude": pin.location.longitude
        }
        for pin in Pin.query.all()
    }

    print pins

    return jsonify(pins)


if __name__ == "__main__":
    # Set debug=True here, since it has to be True at the point
    # of invoking the DebugToolbarExtension

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host="0.0.0.0")
