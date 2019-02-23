from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from pprint import pprint

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/marsApp")

import scrape_mars

@app.route('/')
def home():
    mars_db = mongo.db.mars_db.find_one()
    return(render_template("home.html", mars_db = mars_db))

@app.route('/scrape')
def scraper():
    mars_db = mongo.db.mars_db
    mars_info = scrape_mars.scrape()
    mars_db.update({}, mars_info, upsert=True)
    return redirect("/",code=302)

    #dataDict = scrape_mars.scrape()
    #db.data.insert_one(dataDict)
    #dataDict['_id'] = 1
    #cursor = db.data.find({'_id':1},{'_id':0})
    #for row in cursor:
    #    pprint(row)
    #{'newsTitle': 'After a Reset, Curiosity Is Operating Normally', 
    #'newsPara': "NASA's Mars rover Curiosity is in good health but takes a short break while engineers diagnose why it reset its computer. ", 
    #'featuredImg': 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA17978-1920x1200.jpg', 
    #'marsWeather': 'sol 84 (2019-02-20) low -95.1ºC (-139.2ºF) high -13.2ºC (8.3ºF)', 
    #'marsTable': 'blah'
    # #'hemispheres': [{'title': 'Cerberus Hemisphere', 'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, 
    #    {'title': 'Schiaparelli Hemisphere', 'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}, 
    #    {'title': 'Syrtis Major Hemisphere', 'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, 
    #    {'title': 'Valles Marineris Hemisphere', 'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}]
    #}
    #return(render_template('home.html'))

if __name__ == '__main__':
    app.run(debug=True)