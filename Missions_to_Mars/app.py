from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# To run this project, open app.py in vsc and run this python code by right-click in the code window
#  and choosing the option "Run Python File in Terminal".
# You will see the server started to run and then mouse over the url http://127.0.0.1:5000/ and click on "follow the link"
# hyperlink to go to the homepage. You will see Mars webpage.
# Create an instance of Flask
app = Flask(__name__)


# Use PyMongo to establish Mongo connection: 
# Set up (DB: mars_info_app, Collection: mars_info)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

  # Run scrapped functions
  mars_data = scrape_mars.scrape_mars_news()
  mars_data = scrape_mars.scrape_mars_featured_image()
  mars_f = scrape_mars.scrape_mars_facts()
  mars_data = scrape_mars.scrape_mars_hemi()

  # Update the Mongo database using update and upsert=True
  mars_info = mongo.db.mars_info
  mars_info.update({}, mars_data, upsert=True)

  # Redirect back to home page
  return redirect("/", code=302)
  
if __name__ == "__main__":
    app.run(debug=True)

