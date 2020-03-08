from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd 
import requests


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

mars_data = {}

def scrape_news():
    
    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)

    html_news = browser.html
    soup = bs(html_news, 'html.parser')

    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').find('a').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    return mars_data

    browser.quit()

def scrape_image():

    browser = init_browser()

    space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(space_image_url)
    time.sleep(3)

    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');','')[1:-1]

    nasa_main_url = 'https://www.jpl.nasa.gov'

    featured_image_url = nasa_main_url + featured_image_url

    mars_data['featured_image_url'] = featured_image_url

    return mars_data

    browser.quit()

