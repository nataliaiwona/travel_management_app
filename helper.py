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

    return bcrypt.hashpw(password.encode("UTF_8"),
                     user.password.encode("UTF_8")).decode() == user.password


def check_duplicate_pins(user_id, location, pin_type):
    """Check for existing pin before adding another pin row to database."""

    existing_pin = Pin.query.filter(Pin.user_id == user_id,
                                    Pin.location_id == location.id).first()
    if not existing_pin:
        new_pin = Pin(user_id=user_id,
                      pin_type_id=pin_type, location_id=location.id)
        db.session.add(new_pin)
        db.session.commit()
    else:
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


def edit_pin(user_id, pin_id, pin_type):
    """Edit specific pin in user database."""

    location = Location.query.filter(Location.city == city,
                                     Location.country == country,
                                     Location.latitude == lat,
                                     Location.longitude == lng).first()

    current_pin = Pin.query.filter(Pin.user_id == user_id,
                                   Pin.location_id == location.id).first()
    current_pin.pin_type_id = pin_type
    db.session.commit()


def remove_pin(user_id, pin_id, pin_type):
    """Remove specific pin from user database."""

    current_pin = Pin.query.filter(Pin.user_id == user_id,
                                   Pin.id == pin_id).first()
    db.session.delete(current_pin)
    db.session.commit()










