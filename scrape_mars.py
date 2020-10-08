# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import time
from splinter import Browser
import pandas as pd
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path': '/Users/prashantkapadia/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    executable_path = {'executable_path': '/Users/prashantkapadia/Desktop/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(1)
    
    # Scrape page into Soup
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get the News title and paragraph
    news_title = soup.select_one('ul.item_list li.slide div.content_title a').text
    news_p = soup.select_one('ul.item_list li.slide div.article_teaser_body').text

    ### JPL Mars Space Images - Featured Image
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    time.sleep(1)
    full_image_bt = browser.find_by_id('full_image')
    full_image_bt.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_bt = browser.links.find_by_partial_text('more info')
    more_info_bt.click()
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    image_path = img_soup.select_one('figure.lede a img').get('src')
    featured_image_url = f'https://www.jpl.nasa.gov{image_path}'

    # Mars Weather from Twitter
    twitter_url = ('https://twitter.com/marswxreport?lang=en')
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    time.sleep(1)
    tweets = soup.find("span",text=re.compile("InSight sol"))
    
    # Pulling only text part and assigning to current_weather variable.
    time.sleep(3)
    current_weather = tweets.text
    
    # Mars Hemispheres scrapping image titlel and image URLs.

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemisphere_image_urls = []
    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")
    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()   


    # Store data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image': featured_image_url,
        'current_weather': current_weather,
        'hemisphere_image_urls' : hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
