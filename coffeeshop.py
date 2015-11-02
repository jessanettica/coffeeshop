"""Coffeeshop application Flask server.

"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

import model


app = Flask(__name__)


app.secret_key = 'ahjdsfkjahsdf'


app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/items")
def list_items():
    """Return page showing all the items the coffee shop has to offer"""
    
    items = model.Coffeeshop.get_all()




    return render_template("all_items.html",
                           item_list=items)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    order_total = 0

    # Get the cart (or an empty list if there's no cart)
    raw_cart = session.get('cart', [])

    # Our output cart will be a dictionary (so we can easily see if we
    # already have that item type in there)

    cart = {}

    # Loop over the melon IDs in the session cart and add each one to
    # the output cart

    for item_id in raw_cart:

        # Get the existing item from our output cart, setting to an
        # empty dictionary if not there already
        item = cart.setdefault(item_id, {})

        if item:
            # We've already put melons of this type in our cart, so
            # just up the qty and fix the prices
            item['qty'] += 1

        else:
            # This is the first time we've seen this melon type,
            # so get the info from the database
            item_data = model.Coffeeshop.get_by_id(item_id)

            item['common_name'] = melon_data.common_name
            item['unit_cost'] = melon_data.price
            item['qty'] = 1

        # Either way, let's get the proper total cost and order total

        melon['total_cost'] = melon['unit_cost'] * melon['qty']
        order_total += melon['total_cost']

    # Now, get a list of the all melons we've put into that dict
    cart = cart.values()

    return render_template("cart.html", cart=cart, order_total=order_total)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.
    
    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """

    # Check if we have a cart in the session dictionary and, if not, add one
    cart = session.setdefault('cart', [])

    # Add melon to cart
    cart.append(id)

    # Show user success message on next page load
    flash("Successfully added to cart.")

    # Redirect to shopping cart page
    return redirect("/cart")


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship items."""
    
    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.
    
    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/items")

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    user_firstname = request.form["user_firstname"]
    user_lastname = request.form["user_lastname"]
    user_email = request.form["user_email"]
    user_instagram = request.form["user_instagram"]
    user_city = request.form["user_city"]
    user_password = request.form["user_password"]

    new_user = User(user_firstname=user_firstname, user_lastname=user_lastname, user_email=user_email, user_instagram=user_instagram, user_city=user_city, user_password=user_password)

    db.session.add(new_user)
    db.session.commit()

    flash("Hi %s! Welcome to Andarography." % user_firstname)
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(user_email=email).first()
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.user_password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id
    session["user_firstname"] = user.user_firstname

    flash("Logged in")
    return redirect("/")


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)