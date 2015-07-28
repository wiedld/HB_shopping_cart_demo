"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import model
import os


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = os.environ['FLASK_SECRET_KEY']

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melons = model.Melon.get_all()
    user = session.get('fname', None)

    return render_template("all_melons.html",
                           melon_list=melons, user=user)


@app.route("/melon/<int:id>")
def show_melon(id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = model.Melon.get_by_id(id)
    user = session.get('fname', None)

    return render_template("melon_details.html",
                           display_melon=melon, user=user)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.
    #   - The cart is a list in session containing melons added

    melons_in_cart = session.get('cart', None)
    total = session.get('total', 0)
    user = session.get('fname', None)

    return render_template("cart.html", melons=melons_in_cart, total=total, user=user)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # TODO: Finish shopping cart functionality
    #   - use session variables to hold cart list

    if 'cart' not in session:
        session['cart'] = {}

    melon = model.Melon.get_by_id(id)

    # id: (name, qty, price)
    melon_in_cart = session['cart'].setdefault(str(id), [melon.common_name, 0, melon.price])

    melon_in_cart[1] += 1

    session['total'] = session.get('total', 0) + melon.price

    flash("Melon added to cart.")

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""
    user = session.get('fname', None)

    return render_template("login.html", user=user)


@app.route("/login-process", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    email = request.form.get('email')
    pwd = request.form.get('password')

    customer_obj = model.Customer.get_by_email(email, pwd)

    if customer_obj == "PasswordError":
        flash("You have fat fingers. Enter your password again.")
        return redirect('/login')

    elif customer_obj is not None:
        session['fname'] = customer_obj.fname
        session['lname'] = customer_obj.lname
        return redirect('/melons')
    else:
        flash("You are not registered with the Uber Empire.")
        return redirect('/register')


@app.route("/register")
def register_user():
    """ask user to enter registration info"""
    user = session.get('fname', None)

    return render_template("register.html", user=user)


@app.route("/register-process", methods=["POST"])
def register_process():
    """register a new user, and insert into db"""

    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pwd = request.form.get('password')

    model.Customer.new_customer((email, fname, lname, pwd))

    flash("Please login for the first time.")
    return redirect("/login")


@app.route("/logout-process")
def process_logout():
    session['fname'] = None
    session['lname'] = None
    session['cart'] = {}
    session['total'] = 0

    flash("Logged out.")
    return redirect('/login')


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
