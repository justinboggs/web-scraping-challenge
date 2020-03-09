from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_scraper"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_final = mongo.db.mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars_scrape=mars_final)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_final = scrape_mars.scrape

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_collection.update({}, mars_final, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)