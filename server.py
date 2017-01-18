"""Trippy"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request
from flask import flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Location, Pin
import os
import bcrypt
import helper

app = Flask(__name__)
app.secret_key = "MEMORY"
# For Heroku
# app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")
# app.config['MAPS_KEY'] = os.environ.get("GOOGLE_MAPS_API_KEY", "abcdefg")
maps_key = os.environ["GOOGLE_MAPS_API_KEY"]


# Raises an error for when you use an undefined variable in Jinja2.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True
DebugToolbarExtension(app)


@app.route('/')
def index():
    """Landing page."""

    return render_template("landing_page.html")


@app.route('/guest_login', methods=['GET'])
def guest_login_form():
    """Allow users to access and interact with app without logging in."""

    return render_template("guest_login.html")


@app.route('/guest_login', methods=['POST'])
def guest_login_process():
    """Process guest login."""

    email = "guest@guest.com"
    password = "password"

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user, just click 'Submit'")
        return redirect("/guest_login")

    if not helper.check_pass(user, password):
        flash("Incorrect password, just click 'Submit'")
        return redirect("/guest_login")

    session["user_id"] = user.id
    # flash("You are now logged in as Guest.")

    return redirect("/user_homepage")


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
                    password=bcrypt.hashpw(password.encode("UTF_8"),
                                           bcrypt.gensalt()))

    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    # flash("Thanks for signing up, {}! \
    #       You are now logged in.".format(fname))
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

    if not helper.check_pass(user, password):
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.id
    flash("Welcome, you are now logged in as {}".format(email))

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

    user_id = session.get("user_id")

    if user_id:
        user = User.query.get(user_id)
    else:
        flash("Please log in to add pins to your map.")
        return redirect("/login")

    pin_type = request.form.get("pinTypeId")
    city = request.form.get("city")
    state = request.form.get("state") or None
    country = request.form.get("country")
    lat = request.form.get("latitude")
    lng = request.form.get("longitude")

    location = helper.create_or_get_location(city, state, country, lat, lng)
    new_pin = helper.check_duplicate_pins(user.id, location, pin_type)

    result = {"new_pin_id": new_pin.id}

    return jsonify(result)


@app.route('/user_pin_info.json')
def pin_info():
    """JSON information about user map pins."""

    user_id = session.get("user_id")

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
        for pin in Pin.query.filter(Pin.user_id == user_id).all()
    }

    return jsonify(pins)


@app.route('/edit_pin.json', methods=["POST"])
def update_pin():
    """Edit or delete a specific user pin."""

    pin_id = request.form.get("editPinId")
    pin_type = request.form.get("editPinTypeId")
    city = request.form.get("editPinCity")

    data = helper.edit_pin(pin_id, pin_type, city)
    pin_data = {'lng': data[0],
                'lat': data[1],
                'pin_type': data[2],
                'city': data[3],
                'pin_id': data[4]
                }

    return jsonify(pin_data)


@app.route('/remove_pin.json', methods=["POST"])
def remove_pin():
    """Remove a specific user pin."""

    pin_id = request.form.get("id")

    lnglat = helper.remove_pin(pin_id)
    pin_data = {'lng': lnglat[0],
                'lat': lnglat[1]
                }

    return jsonify(pin_data)


# if __name__ == "__main__":
#     # Set debug=True here, since it has to be True at the point
#     # of invoking the DebugToolbarExtension

#     connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    db.create_all(app=app)
    
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)