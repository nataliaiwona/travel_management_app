"""Utility file to seed travel information data in seed_data/"""

from sqlalchemy import func

from model import User, PinType, Location, Pin, connect_to_db, db
from server import app


def load_users():
    """Load users from users.csv into database."""

    User.query.delete()

    print "Users"

    for i, row in enumerate(open("seed_data/users.csv")):
        row = row.rstrip()
        id, fname, lname, email, password = row.split(",")

        user = User(id=id, 
                    fname=fname, 
                    lname=lname,
                    email=email,
                    password=password)

        # Add to session so it will be stored!
        db.session.add(user)

        # Show progress
        if i % 100 == 0:
            print i

    # Commit above work
    db.session.commit()


def load_pin_types():
    """Load pin types from pin_types.csv into database."""

    PinType.query.delete()

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

    Location.query.delete()

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

    Pin.query.delete()

    print "Pins"

    for i, row in enumerate(open("seed_data/pins.csv")):
        row = row.rstrip()
        id, user_id, pin_type_id, location_id, visits, year = row.split(",")

        pins = Pin(id=id, 
                   user_id=user_id,
                   pin_type_id=pin_type_id,
                   location_id=location_id,
                   visits=visits,
                   year=year)

        db.session.add(pins)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # For loop? Get the Max user_id in the database
    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_pin_types()
    load_locations()
    load_pins()
    set_val_user_id()
