"""Models and database functions for Coffeeshop"""

from flask_sqlalchemy import SQLAlchemy
#import os

db = SQLAlchemy()

print 'Model was imported'

##############################################################################


class Merchant(db.Model):
    """Info about the merchant using the web app."""

    __tablename__ = "merchants"

    merchant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    merchant_firstname = db.Column(db.String(64))
    merchant_lastname = db.Column(db.String(64), nullable=True)
    merchant_email = db.Column(db.String(64))
    merchant_city = db.Column(db.String(64), nullable=True)
    merchant_password = db.Column(db.String(64))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Merchant merchant_id=%s username=%s>" % (self.user_id, self.user_email)


class Item(db.Model):
    """Coffeeshop items offered."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.String(64))
    item_currency = db.Column(db.String(4))
    item_price = db.Column(db.Integer, nullable=True)
    item_category = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    category = db.relationship("Category", backref=db.backref("items", order_by=item_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Item item_id=%s item_category=%s>" % (self.item_id, self.item_category)


class Payment(db.Model):
    """Payment occured for a coffee shop item."""

    __tablename__ = "payments"

    payment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('merchants.merchant_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'))
    purchase_datetime = db.Column(db.DateTime)

    merchant = db.relationship("Merchant", backref=db.backref("payments", order_by=payment_id))

    item = db.relationship("Item", backref=db.backref("payments", order_by=payment_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Payment payment_id=%s merchant_id=%s item_id=%s " % (
            self.payment_id, self.merchant_id, self.item_id)



class Category(db.Model):
    """Categories for experiences and activities."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category_name=%s " % (
            self.category_id, self.category_name)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee.db'
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 
# 'postgres://lusjbdzibnxhjb:4HNukyWbMYWUV7ZyIzyITIFcxv@ec2-54-83-57-86.compute-1.amazonaws.com:5432/dkp7hqct3tajs',
#         )
    db.app = app
    #connecting model and database
    db.init_app(app)


if __name__ == "__main__":

    from coffeeshop import app
    connect_to_db(app)
    print "Connected to DB."