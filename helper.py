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

    return bcrypt.hashpw(password.encode("UTF_8"),
                     user.password.encode("UTF_8")).decode() == user.password


def create_or_update_pin(user_id, location, pin_type):

    existing_pin = Pin.query.filter(Pin.user_id == user_id,
                                    Pin.location_id == location.id).first()
    if not existing_pin:
        new_pin = Pin(user_id=user.id,
                      pin_type_id=pin_type, location_id=location.id)
        db.session.add(new_pin)
        db.session.commit()
    else:
        existing_pin.pin_type_id = pin_type
        db.session.commit()


def create_or_get_location(city, state, country, lat, lng):
    location = Location.query.filter(Location.city == city,
                                     Location.country == country,
                                     Location.latitude == lat,
                                     Location.longitude == lng).first()
    if location is None:
        location = Location(city=city, state=state, country=country,
                            latitude=lat, longitude=lng)
        db.session.add(location)
        db.session.commit()
