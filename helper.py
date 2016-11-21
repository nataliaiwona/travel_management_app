from jinja2 import StrictUndefined
from flask import Flask, render_template, request
from flask import flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Location, Pin
import os
import bcrypt
import server

app = Flask(__name__)
app.secret_key = "MEMORY"


def check_pass(user, password):
    """Check that password matches user."""

    p = bcrypt.hashpw(password.encode("UTF_8"),
                      user.password.encode("UTF_8")).decode() == user.password

    return p


def check_duplicate_pins(user_id, location, pin_type):
    """Check for existing pin before adding another pin row to database."""

    existing_pin = Pin.query.filter(Pin.user_id == user_id,
                                    Pin.location_id == location.id).first()
    if not existing_pin:
        new_pin = Pin(user_id=user_id,
                      pin_type_id=pin_type, location_id=location.id)
        db.session.add(new_pin)
        db.session.commit()

        return new_pin

    else:
        # TODO need error handling so can't edit pin through modal
        existing_pin.pin_type_id = pin_type
        db.session.commit()

def create_or_get_location(city, state, country, lat, lng):
    """Create new location or get existing location from database"""

    location = Location.query.filter(Location.city == city,
                                     Location.country == country,
                                     Location.latitude == lat,
                                     Location.longitude == lng).first()
    if location is None:
        location = Location(city=city, state=state, country=country,
                            latitude=lat, longitude=lng)
        db.session.add(location)
        db.session.commit()

    return location


def edit_pin(pin_id, pin_type, city):
    """Edit specific pin in user database."""

    current_pin = Pin.query.get(pin_id)

    lng = current_pin.location.longitude
    lat = current_pin.location.latitude
    city = current_pin.location.city
    pin_id = current_pin.id

    current_pin.pin_type_id = pin_type
    db.session.commit()

    return [lng, lat, pin_type, city, pin_id]


def remove_pin(pin_id):
    """Remove specific pin from user database."""

    current_pin = Pin.query.get(pin_id)

    lng = current_pin.location.longitude
    lat = current_pin.location.latitude

    db.session.delete(current_pin)
    db.session.commit()

    return [lng, lat]




