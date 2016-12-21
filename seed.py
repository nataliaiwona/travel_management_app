"""Utility file to seed travel information data in seed_data/"""

from sqlalchemy import func

from model import User, PinType, Location, Pin, connect_to_db, db
from server import app

import bcrypt


def load_users():
    """Load users from users.csv into database."""

    print "Users"

    for row in open("seed_data/users.csv"):
        row = row.rstrip()
        id, fname, lname, email, password = row.split(",")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=bcrypt.hashpw(password, bcrypt.gensalt()))

        db.session.add(user)

    db.session.commit()

 
def load_pin_types():
    """Load pin types from pin_types.csv into database."""

    print "Pin Types"

    for row in open("seed_data/pin_types.csv"):
        row = row.rstrip()
        id, description = row.split(",")

        pin_types = PinType(id=id,
                            description=description)

        db.session.add(pin_types)

    db.session.commit()


def load_locations():
    """Load locations from locations.csv into database."""

    print "Locations"

    for row in open("seed_data/locations.csv"):
        row = row.rstrip().split(",")

        for i, element in enumerate(row):
            if element == "":
                row[i] = None

        id, city, state, country, latitude, longitude = row

        locations = Location(city=city,
                             state=state,
                             country=country,
                             latitude=latitude,
                             longitude=longitude,)

        db.session.add(locations)

    db.session.commit()


def load_pins():
    """Load pins from pins.csv into database."""

    print "Pins"

    for row in open("seed_data/pins.csv"):
        row = row.rstrip().split(",")

        for i, element in enumerate(row):
            if element == "":
                row[i] = None

        id, user_id, pin_type_id, location_id = row

        pins = Pin(user_id=user_id,
                   pin_type_id=pin_type_id,
                   location_id=location_id
                   )

        db.session.add(pins)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_location_id():
    """Set value for the next location_id after seeding database"""

    result = db.session.query(func.max(Location.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('locations_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_pin_id():
    """Set value for the next pin_id after seeding database"""

    result = db.session.query(func.max(Pin.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('pins_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    print "Connecting"
    connect_to_db(app)
    print "Dropping"
    db.drop_all()   # solving cascade delete
    print "Creating"
    db.create_all()

    load_pin_types()
    load_users()
    load_locations()
    load_pins()

    set_val_user_id()
    set_val_location_id()
    set_val_pin_id()
