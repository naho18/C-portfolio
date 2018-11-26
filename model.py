"""Model for C-Portfolio database"""

#import library
from flask_sqlalchemy import SQLAlchemy

#create database
db = SQLAlchemy()

##############################################################################
# create model for each table

class User(db.Model):
    """User of C-Portfolio"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Show information about users"""

        return "<user_id= %s name= %s>" % (self.user_id, self.name)


class Investment(db.Model):
    """Investments in Portfolio"""

    __tablename__ = "investments"

    inv_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_entry = db.Column(db.Date)
    date_of_investment = db.Column(db.Date)
    company_name = db.Column(db.String(32), nullable=False)
    quantity = db.Column(db.Integer)
    cost = db.Column(db.Integer)

    def __repr__(self):
        """Show information about investments"""

        return "<company_name= %s date_of_investment= %s cost= %d>" % (
            self.company_name, self.date_of_investment, self.cost)


class UserInv(db.Model):
    """Users' investments"""

    __tablename__ = "userinv"

    userinv_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    inv_id = db.Column(db.Integer, db.ForeignKey('investments.inv_id'), nullable=False)

    # create relationship with User and Food tables
    user = db.relationship('User', backref='userinv')
    inv = db.relationship('Investment', backref='userinv')

    def __repr__(self):
        """Shows information about users' investments"""

        return "<userinv_id= %d user_id= %d inv_id= %d>" % (
            self.userinv_id, self.user_id, self.inv_id)

##############################################################################
# use helper functions to connect to database and add example data

def connect_to_db(app, db_uri='postgresql:///c-portfolio'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # connect db to app
    db.app = app
    db.init_app(app)

def example_data():
    """Example data for test database"""

    # USERS
    u1 = User(name='John Doe', email='jd@gmail.com', password='jd123')
    u2 = User(name='Chase Bunny', email='cb@gmail.com', password='cb123')
    u3 = User(name='Phoebe Buffay', email='pb@gmail.com', password='pb123')

    db.session.add_all([u1, u2, u3])
    db.session.commit()

    # INVESTMENTS
    inv1 = Investment(date_of_entry='2018-11-25', date_of_investment='2018-11-25',
        company_name='eggAmple', quantity='50000', cost='100000')
    inv2 = Investment(date_of_entry='2018-11-25', date_of_investment='2018-11-26',
        company_name='giveThanks', quantity='100000', cost='250000')
    inv3 = Investment(date_of_entry='2018-11-25', date_of_investment='2018-11-25',
        company_name='wonderFull', quantity='50000', cost='150000')

    db.session.add_all([inv1, inv2, inv3])
    db.session.commit()

    # USERINV
    uinv1 = UserInv(user_id='1', inv_id='1')
    uinv2 = UserInv(user_id='1', inv_id='2')
    uinv3 = UserInv(user_id='2', inv_id='3')

    db.session.add_all([uinv1, uinv2, uinv3])
    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

# db.create_all()
