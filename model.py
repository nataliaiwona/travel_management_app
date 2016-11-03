"""Models and database functions for Travel Diary project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of travel diary website."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

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
    name = db.Column(db.String(35), nullable=False)
    city = db.Column(db.String(35), nullable=False)
    state = db.Column(db.String(35), nullable=True)
    country = db.Column(db.String(35), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """Provide helpful representation of location info when printed."""

        l = "<Location id={} name={} city={} country={} latitude={} longitude={}>"
        return l.format(
            self.id, self.name, self.city, self.country,
            self.latitude, self.longitude)


class Pin(db.Model):
    """Pins users have pinned to travel diary website."""

    __tablename__ = "pins"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pin_type_id = db.Column(db.Integer, db.ForeignKey('pin_types.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    year = db.Column(db.Integer, nullable=True)
    visits = db.Column(db.Integer, nullable=True)

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

        p = "<Pins id={} user_id={} pin_type_id={} location_id={} year={} visits={}>"
        return p.format(self.id, self.user_id, self.pin_type_id,
                        self.location_id, self.year, self.visits)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///travels'

    # app.config['SQLAlCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # If running module interactively, it will be in a state of being
    # able to work with the database directly.
    from server import app

    connect_to_db(app)
    print "Connected to DB."
