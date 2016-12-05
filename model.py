import sys
from flask_sqlalchemy import SQLAlchemy
reload(sys)
sys.setdefaultencoding('utf-8')

"""Models and database functions for Travel Diary project."""

db = SQLAlchemy()


class User(db.Model):
    """User of travel diary website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation of user info when printed."""

        return "<User id={} {} {} email={}>".format(
            self.id, self.fname, self.lname, self.email)


class PinType(db.Model):
    """Pin type associated with travel diary website."""

    __tablename__ = "pin_types"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """Provide helpful representation of pin type info when printed."""

        return "<Pin type id={} description={}>".format(
            self.id, self.description)


class Location(db.Model):
    """User of travel diary website."""

    __tablename__ = "locations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """Provide helpful representation of location info when printed."""

        l = "<Location id={} city={} country={} latitude={} longitude={}>"
        return l.format(
            self.id, self.city, self.country,
            self.latitude, self.longitude)


class Pin(db.Model):
    """Pins users have pinned to travel diary website."""

    __tablename__ = "pins"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pin_type_id = db.Column(db.Integer, db.ForeignKey('pin_types.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("pins", order_by=id))
    # Define relationship to pin type
    pin_type = db.relationship("PinType",
                               backref=db.backref("pins", order_by=id))

    # Define relationship to location
    location = db.relationship("Location",
                               backref=db.backref("pins", order_by=id))

    def __repr__(self):
        """Provide helpful representation of pins info when printed."""

        p = "<Pins city={} name={} user_id={} pin={} pin_type_id={} \
            location_id={}>"
        return p.format(self.location.city, self.user.fname, self.user_id,
                        self.pin_type.description, self.pin_type_id,
                        self.location_id)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DB_URI'] = db_uri or 'postgresql:///travels'

    # app.config['SQLAlCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    print "Connected to DB."


def example_data():
    """Sample user data."""

    user1 = User(fname="Dale", lname="Cooper", email="dale.cooper@fbi.com",
                 password="damngoodcoffee")

    db.session.add(user1)
    db.session.commit()
    user_id = db.session.query(User.id).filter(User.email == "dale.cooper@fbi.com").first()

    location1 = Location(id="3", city="Twin Peaks", state="Washington",
                         country="United States", latitude=47.9556626,
                         longitude=-121.3809409)
    db.session.add(location1)
    db.session.commit()

    pin1 = Pin(user_id=user_id[0], location_id="3", pin_type_id="2")

    db.session.add(pin1)
    db.session.commit()

if __name__ == "__main__":
    # If running module interactively, it will be in a state of being
    # able to work with the database directly.
    from server import app

    connect_to_db(app)
    print "Connected to DB."
