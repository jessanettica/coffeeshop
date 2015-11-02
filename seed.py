"""Utility file to seed coffeeshop database from data in seed_data/"""

import datetime
import requests
from model import connect_to_db, db, Item, Merchant, Payment, Category
from coffeeshop import app
import os


def load_categories():
    """Load categories from u.categories into database"""

    for row in open("seed_data/u.categories"):

        category_name = row

        category = Category(category_name=category_name)

        db.session.add(category)

    db.session.commit()

def load_items():
    """Load items from u.items into database."""

    print "Items"

    for i, row in enumerate(open("seed_data/u.items")):
        row = row.rstrip()

        item_name, item_category, item_currency, item_price = row.split("|")


        item = Item(item_name=item_name, item_category=item_category, item_currency=item_currency, item_price=item_price)
        db.session.add(item)

        if i % 100 == 0:
            print i

	db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_categories()
    load_items()
