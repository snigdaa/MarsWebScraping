#!/usr/bin/env python
# coding: utf-8


def scrape():  
       
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    import pandas as pd

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    newshtml = browser.html
    soup = bs(newshtml, 'html.parser')
    news_title = soup.find("h3").text
    news_p = soup.find("div",class_="rollover_description_inner").text



    #JPL Mars Space Images - Featured Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    jplhtml = browser.html
    soup = bs(jplhtml, 'html.parser')
    #image url is inside an article tag in the 'style' parameter, which is why
    #we're accessing it below like so
    imageExt = soup.article['style'][23:-3]
    featured_image_url = 'https://www.jpl.nasa.gov' + imageExt



    #Mars Weather
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    twitterhtml = browser.html
    soup = bs(twitterhtml, 'html.parser')
    #Find the tweets
    tweets = soup.find_all("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    #Get the first tweet
    count = 1
    recentTweets = []
    for tweet in tweets:
        #make sure it's a weather tweet
        if "pressure at" in tweet.text or "winds from the" in tweet.text:
            startIdx = tweet.text.lower().index("sol")
            if "\n" in tweet.text:
                endIdx = tweet.text.index("\n")
                recentTweets.append(tweet.text[startIdx:endIdx])
                if count == 1:
                    mars_weather = tweet.text[startIdx:endIdx]
                    count +=1
            else:
                recentTweets.append(tweet.text[startIdx:])
                if count == 1:
                    mars_weather = tweet.text[startIdx:]
                    count +=1


    #Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    factshtml = browser.html
    soup = bs(factshtml, 'html.parser')
    table = soup.find_all("table", {'id':'tablepress-mars'})
    #go through the soup table object and make it an html string
    io = ""
    for item in table:
        io = io + str(item)
    marslist = pd.read_html(io)
    #choose the dataframe from list of dataframes since read_html returns a list not a df directly
    df = marslist[0]
    #rename the '0' and '1' columns with meaningful titles
    df = df.rename(columns = {0:'Description', 1:'Value'}).set_index('Description')
    #make an html string to represent the dataframe
    dfhtml = df.to_html()



    #Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    hemhtml = browser.html
    soup = bs(hemhtml, 'html.parser')
    hemUrls = []
    links = soup.find_all("div", class_="item")
    #go through each of the hemispheres and get their links
    for link in links:
        imglink = "https://astrogeology.usgs.gov" + link.a['href']
        hemUrls.append(imglink)
    #visit each of the image links to get the actual image url and hemisphere name
    hemisphere_image_urls = []
    for idx, val in enumerate(hemUrls):
        url = val
        browser.visit(url)    
        imghtml = browser.html
        soup = bs(imghtml, 'html.parser')
        #get the html sections that have the image url    
        imgs = soup.find_all("img", class_ = "wide-image")
        name = soup.find("h2",class_="title")
        #get the image url (will only go through loop once for each hemisphere)    
        for content in imgs:
            img_url = 'https://astrogeology.usgs.gov' + content["src"]    
        #append a dictionary to list of dicts for each image
        hemisphere_image_urls.append({'title': name.text[:-9], 'img_url' : img_url})


    #Now put everything in a dictionary to pass to MongoDB
    ultimate = {
        'newsTitle':news_title,
        'newsPara':news_p,
        'featuredImg':featured_image_url,
        'marsWeather':mars_weather,
        'marsTable':dfhtml,
        'hemispheres':hemisphere_image_urls
    }

    return(ultimate)