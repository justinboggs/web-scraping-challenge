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

    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mongo.db.mars_data
    mars_data2 = scrape_mars.scrape_news()
    mars_data2 = scrape_mars.scrape_image()
    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_data2, upsert=True)

    # Update the Mongo database using update and upsert=True

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)