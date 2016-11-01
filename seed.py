"""Utility file to seed travel information data in seed_data/"""

from slqalchemy import func

from model import User, PinType, Location, Pin, connect_to_db, connect_to_db
from server import app


def load_users():
    """Load users from users.csv into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/users.csv")):
        row = row.rstrip()
        id, fname, lname = row.split(",")

        user = User(id=id, 
                    fname=fname, 
                    lname=lname)

        # Add to session so it will be stored!
        db.session.add(user)

        # Show progress
        if i % 100 == 0:
            print i

    # Commit above work
    db.session.commit()


def load_pin_types():
    """Load pin types from pin_types.csv into database."""

    print "Pin Types"

    for i, row in enumerate(open("seed_data/pin_types.csv")):
        row = row.rstrip()
        id, description = row.split(",")

        pin_types = PinType(id=id, 
                            description=description)

        db.session.add(pin_types)

    db.session.commit()


def load_locations():
    """Load locations from locations.csv into database."""

    print "Locations"

    for i, row in enumerate(open("seed_data/locations.csv")):
        row = row.rstrip()
        id, name, city, state, country, latitude, longitude = row.split(",")

        location = Location(id=id, 
                            name=name,
                            city=city,
                            state=state,
                            country=country,
                            latitude=latitude,
                            longitude=longitude)

        db.session.add(location)

    db.session.commit()


def load_pins():
    """Load pins from pins.csv into database."""

    print "Pins"

    for i, row in enumerate(open("seed_data/pins.csv")):
        row = row.rstrip()
        id, user_id, pin_type_id, location_id, visits, year = row.split(",")

        pins = Pin(id=id, 
                   user_id=user_id,
                   pin_type_id=pin_type_id,
                   location_id=location_id,
                   visits=visits,
                   year=year
                   )

        db.session.add(pins)

    db.session.commit()
