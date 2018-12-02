"""Server for Portfolio"""

#import library & modules & files
from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Investment, UserInv

import datetime
import string
from jinja2 import StrictUndefined

import unirest
import os

from flask import jsonify
from sqlalchemy import update


# create flask app
app = Flask(__name__)

# create secret key
app.secret_key = os.environ['FLASK_SECRET_KEY']

# raises jinja underfined error
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():

        return render_template('c-portfolio.html')


@app.route('/registration', methods=['POST'])
def register_user():
    """Registers user"""

    user_name = request.form['name']
    user_email = request.form['email']
    user_password = request.form['password']

    # Check to see if user already exists
    email_query = User.query.filter_by(email=user_email).all()

    if email_query:
        flash('Already a member. Please log in')
        return redirect('/')
    else:
        # Add user to database
        user = User(name=user_name, email=user_email, password=user_password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in!')
        return redirect('/')


@app.route('/login', methods=['POST'])
def login_check():
    """Validates user info, takes user to home page"""

    # Get user email & password from form
    user_email = request.form['email']
    user_password = request.form['password']

    # Check user info against database
    email_query = User.query.filter_by(email=user_email).first()
    if email_query == None:
        flash('Invalid email or password')
        return redirect('/')

    # Get user's id using email
    user_id = email_query.user_id

    # Valid user password
    if user_password == email_query.password:
        #create user session
        session['user'] = email_query.user_id
        return redirect('/user-%s' % user_id)
    else:
        flash('Invalid email or password')
        return redirect('/')


@app.route('/logout')
def logout():
    """logs user out of session"""
    if session:
        session.pop('user')
        flash('You were successfully logged out')
        return redirect('/')
    else:
        return redirect('/')


# display current inv
@app.route('/user-<user_id>')
def display_homepage(user_id):
    """Show current investments in Portfolio"""

    user_inv = (UserInv.query.filter_by(user_id=user_id)).all()

    # current_inv = []

    # list of all user's investments 
    # for item in user_inv:
    #     current_inv.append({'company': item.inv.company_name, 'quantity': 
    #         item.inv.quantity, 'cost': item.inv.cost})

    return render_template('user-homepage.html',
                            user_inv=user_inv)


@app.route('/investments-by-date.json')
def find_by_date():
    """Returns the state of all investments on a given date"""

    input_date = request.args.get('date')
    print 'input date', input_date
    
    user_id = session['user']
    user_inv = (UserInv.query.filter_by(user_id=user_id)).all()

    inv_by_date = []

    for item in user_inv:    
        if str(item.inv.date_of_investment) == input_date:
            inv_by_date.append({'company': item.inv.company_name, 'quantity': 
                item.inv.quantity, 'cost': item.inv.cost})

    print 'inv by date', inv_by_date

    # inv_results = str(inv_by_date)

    return jsonify(inv_by_date)


@app.route('/add-investment.json', methods=['POST'])
def add_investment():
    """Adds investment and updates database"""

    company_name = request.form['company-name']
    date_of_entry = datetime.datetime.today().strftime('%Y-%m-%d')
    
    input_quantity = request.form['quantity']
    # quantity = int(str(input_quantity).replace(',', ''))
    
    input_cost = request.form['cost']
    # cost = int(str(input_cost).replace(',', ''))
    date_of_investment = request.form['inv-date']

    print 'doi ', date_of_investment

    # new_inv = Investment(date_of_investment=date_of_investment, 
    #     company_name=company_name, quantity=quantity, cost=cost)
    
    # db.session.add(new_inv)
    # db.session.commit()

    return jsonify('investment added!')



##############################################################################


if __name__ == "__main__":
    # app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run('0.0.0.0')
