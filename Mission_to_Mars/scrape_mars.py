from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd 
import requests
import pymongo

def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape():
    
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)

    #Mars News
    html_news = browser.html
    soup = bs(html_news, 'html.parser')

    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').find('a').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text


    #Mars Image
    space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)
    time.sleep(3)

    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');','')[1:-1]

    nasa_main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = nasa_main_url + featured_image_url


    #Mars Twitter
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(3)

    twitter_html_content = requests.get(twitter_url).text
    soup = bs(twitter_html_content, 'lxml')

    tweet_list = soup.find_all('div', class_="js-tweet-text-container")
    holds_tweet = []
    for tweets in tweet_list: 
        tweet_body = tweets.find('p').text
        if 'InSight' and 'sol' in tweet_body:
            holds_tweet.append(tweet_body)
            break
        else: 
            pass

    mars_weather = ([holds_tweet[0]][0][:-26])
    tweet_img_link = ([holds_tweet[0]][0][-26:])


    # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(3)

    mars_data = pd.read_html(facts_url)
    mars_facts = mars_data[0]
    mars_facts.columns = ['Description', 'Stats']
    mars_facts = mars_facts.to_html()


    #Mars Hemispheres
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    time.sleep(3)

    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    images = soup.find_all('div', class_='item')
    hemi_images = []
    hemi_main_url = 'https://astrogeology.usgs.gov/'

    for img in images:
        hemi_title = img.find('h3').text
        hemi_url = img.find('a', class_='itemLink product-item')['href']
        browser.visit(hemi_main_url + hemi_url)
        time.sleep(3)
        hemi_url = browser.html
        soup = bs(hemi_url, 'html.parser')
        full_url = hemi_main_url + soup.find('img', class_='wide-image')['src']
        hemi_images.append({'title': hemi_title, 'img_url': full_url})


    #Store all gathered data
    mars_final = {
        news_title,
        news_paragraph,
        featured_image_url,
        mars_weather,
        hemi_images
    }

    browser.quit()

    return mars_final