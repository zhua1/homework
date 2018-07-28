import scrape_mars
from pymongo import MongoClient
from flask import Flask, render_template, redirect

app = Flask(__name__)

# Put scraped data into MongoDB
@app.route("/scrape")
def mongoStuff():
    # Pymongo stuff
    client = MongoClient('localhost', 27017) 
    db = client['config']
    if 'mars' in db.list_collection_names():
        db.drop_collection('mars')
    collection = db['mars']
    # Get dictionary
    d = scrape_mars.scrape()
    # Insert dictionary into MongoDB
    collection.insert_one(d)
    return(redirect("/"))

@app.route("/")
def showHTML():
    # Fetch data from MongoDB
    client = MongoClient('localhost', 27017)
    db = client['config']
    collection = db['mars']
    data = collection.find_one()
    title = data['title']
    image_url = data['image_url']
    paragraph = data['paragraph']
    weather = data['mar_weather']
    html_table = data['html_table']
    images = data['hemisphere_image_urls']
    
    return(render_template("index.html", title = title, paragraph = paragraph, image_url = image_url, weather = weather, html_table = html_table, images=images))


if __name__ == "__main__":
    app.run(port = 5000, debug=True)