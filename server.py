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
app.secret_key = "examplepassword"

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

    return render_template('user-homepage.html',
                            user_inv=user_inv)


@app.route('/investments-by-date.json')
def find_by_date():
    """Returns the state of all investments on a given date"""

    input_date = request.args.get('date')
    
    user_id = session['user']
    user_inv = (UserInv.query.filter_by(user_id=user_id)).all()

    inv_by_date = []

    for item in user_inv:    
        if str(item.inv.date_of_investment) == input_date:
            inv_by_date.append({"company": item.inv.company_name, 
                                "quantity": item.inv.quantity, 
                                "cost": item.inv.cost})
    print inv_by_date

    return jsonify(inv_by_date)


@app.route('/add-investment.json')
def add_investment():
    """Adds investment and updates database"""

    company_name = request.args.get('company-name')
    date_of_entry = datetime.datetime.today().strftime('%Y-%m-%d')
    
    input_quantity = request.args.get('quantity')
    quantity = int(str(input_quantity).replace(',', ''))
    
    input_cost = request.args.get('cost')
    cost = int(str(input_cost).replace(',', ''))

    date_of_investment = request.args.get('date')

    new_inv = Investment(date_of_entry=date_of_entry, 
                        date_of_investment=date_of_investment,
                        company_name=company_name, 
                        quantity=quantity, 
                        cost=cost)
    
    db.session.add(new_inv)
    db.session.commit()

    user_id = session['user']
    new_inv_id = new_inv.inv_id


    new_userinv = UserInv(inv_id=new_inv_id,
                            user_id=user_id)
    db.session.add(new_userinv)
    db.session.commit()

    return jsonify('investment added!')


@app.route('/update-investment.json')
def update_investment():
    """Updates investment in database"""

    user_id = session['user']
    inv_id = request.args.get('update-inv')
    input_quantity = request.args.get('quantity')
    quantity = int(str(input_quantity).replace(',', ''))
    input_cost = request.args.get('cost')
    cost = int(str(input_cost).replace(',', ''))
    date_of_investment = request.args.get('inv-date')

    # Query selected investment to update
    updated_inv = Investment.query.get(inv_id)
    updated_inv.quantity = quantity
    updated_inv.cost = cost
    updated_inv.date_of_investment = date_of_investment

    db.session.commit()

    return redirect('/user-%s' % user_id)

##############################################################################


if __name__ == "__main__":
    # app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run('0.0.0.0')
