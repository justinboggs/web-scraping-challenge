from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# create instance of Flask app
app = Flask(__name__)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", vacation=destination_data)


if __name__ == "__main__":
    app.run(debug=True)