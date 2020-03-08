from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd 
import requests


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}

def scrape_news():
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(3)

    html_news = browser.html
    soup = BeautifulSoup(html_news, 'html.parser')

    news_title = soup.find('div', class_='list_text').find('div', class_='content_title').find('a').text
    news_paragraph = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    return mars_data

    browser.quit()
