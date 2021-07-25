# Declare Dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import warnings
import pandas as pd
import os

# warnings.filterwarnings('ignore')

## define a global variable to store the data from MongoDB
mars_info_dict = {}

## Set up Splinter
def setup_splinter():
  # @NOTE: Path to the local chromedriver
  # executable_path = {"executable_path": "C:\xx\Users\\charm\\Desktop\chromedriver"}
  executable_path = {'executable_path': ChromeDriverManager().install()}
  browser = Browser('chrome', **executable_path, headless=False)
  return browser

##--------------------
## Mars News from NASA
##--------------------
def scrape_mars_news():
  # Set up Splinter
  browser = setup_splinter()

  # Visit NASA MARS News Site that to be scraped
  news_url = 'https://mars.nasa.gov/news/'
  browser.visit(news_url)
  time.sleep(3)

  # Scrape page into Soup
  news_html = browser.html
  news_soup = bs(news_html, "html.parser")
  list_text_all = news_soup.find_all('div', class_='list_text')
  ## scrape the first result from the ResultSet (list_text_all):
  content_title = list_text_all[0].find('div', class_ = 'content_title')
  news_title = content_title.text.strip()

  news_paragraph = list_text_all[0].find('div', class_ = 'article_teaser_body')
  news_p = news_paragraph.text.strip()

  ## Save the data to mars_info
  mars_info_dict['news_title'] = news_title
  mars_info_dict['news_paragraph'] = news_p

  return mars_info_dict

##---------------------------------------
## JPL Mars Space Images - Featured Image
##---------------------------------------
def scrape_mars_featured_image():
  # Set up Splinter
  browser = setup_splinter()

  nasa_url = 'https://www.jpl.nasa.gov'
  image_url = 'https://www.jpl.nasa.gov/images?search=&category=Mars'
  # img_download_url = 'https://www.jpl.nasa.gov/images/baldet-crater-false-color-2'

  browser.visit(image_url)
  time.sleep(3)

  # Scrape page into Soup
  img_html = browser.html

  ## Parse HTML
  img_soup = bs(img_html, "html.parser")

  ## retrieve the list of relative URL for image detail page, where the download button can be found to a full-size image
  ## Found this HTML via Inspecting page source: <a href="/images/black-and-white-view-of-ingenuitys-fourth-flight" class="group  cursor-pointer block">
  image_detail_page_all = img_soup.select('a[href^="/images/"]')

  ## Debug: Check a list of relative url to the detailed image page
  # for i in image_detail_page_all:
  #     print(i['href'])
      
  ## Pick an image's relative URL, contruct a full url by prefixing the nasa_url.
  image_detail_page_url = nasa_url + image_detail_page_all[1]['href']

  print(f"image_detail_url = {image_detail_page_url}")

  ## Part 2: Get the full image URL: 
  ## Visit the image detail page
  browser.visit(image_detail_page_url)
  time.sleep(3)

  # Scrape page into Soup
  img_detail_html = browser.html

  ## Parse HTML to find the URL for the full featured image: <a data-v-0526c969="" href="https://d2pn8kiwq2w21t.cloudfront.net/original_images/jpegPIA24647.jpg" class="BaseButton text-contrast-none w-full mb-5 -primary -compact inline-block"><span class="label block">Download JPG </span></a>
  img_detail_soup = bs(img_detail_html, "html.parser")

  ## find the "a" tag with href contains "original_images", save the URL
  featured_full_image_url = img_detail_soup.select('a[href*="original_images"]')[0]['href']

  print(f"The featured_full_image_url = {featured_full_image_url}")

  mars_info_dict['full_featured_image_url'] = featured_full_image_url

  browser.quit()
  return mars_info_dict

##------------------------
## Mars Facts
##------------------------
def scrape_mars_facts():
  # Set up Splinter
  browser = setup_splinter()

  # Visit Mars Facts page for Mars' facts
  mars_facts_url = "https://galaxyfacts-mars.com/"
  browser.visit(mars_facts_url)
  html = browser.html

  # Use Pandas to scrape the fact table about Mars
  mars_facts_tables = pd.read_html(mars_facts_url)
  mars_facts_df = mars_facts_tables[0]

  # Rename columns
  mars_facts_df.columns = ['Description','Mars', 'Earth']

  # Reset Index to be description
  mars_facts_df.set_index('Description', inplace=True)

  # Use Pandas to convert the data to a HTML table string
  mars_fact_tbl = mars_facts_df.to_html()

  # Save the information
  mars_info_dict['facts_table'] = mars_fact_tbl

  browser.quit()
  return mars_info_dict


##--------------------------------------
## Mars Hemisphere
##--------------------------------------
def scrape_mars_hemi():
  # Set up Splinter
  browser = setup_splinter()

  hemi_url = 'https://marshemispheres.com/'
  # img_download_url = 'https://www.jpl.nasa.gov/images/baldet-crater-false-color-2'

  browser.visit(hemi_url)
  time.sleep(3)

  # Scrape page into Soup
  html_hemi = browser.html

  # Parse HTML with Beautiful Soup
  soup = bs(html_hemi, 'html.parser')

  # Retreive all 4 items that contain mars hemispheres information
  items_all = soup.find_all('div', class_='item')
  # print(items_all)

  # Create an empty list for hemisphere urls 
  hemi_image_urls = []

  # Loop through all 4 items
  for item in items_all: 
    # Store title
    title = item.find('h3').text
    
    # save the partial image URL
    partial_img_url = item.find('a', class_='itemLink product-item')['href']
    
    # Go to the image link
    browser.visit(hemi_url + partial_img_url)
    
    # HTML Object of individual hemisphere information website 
    partial_img_html = browser.html
    
    # Parse HTML with Beautiful Soup for each hemisphere website 
    soup = bs( partial_img_html, 'html.parser')
    
    # Retrieve the full image source from html tag "<img class="wide-image" src="/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg">"
    full_img_url = hemi_url + soup.find('img', class_='wide-image')['src']
    
    # Append the retreived information into a dict list 
    hemi_image_urls.append({"title" : title, "full_img_url" : full_img_url})
    
  # # Display hemisphere_image_urls
  # hemi_image_urls
    
  # Display hemisphere_image_urls
  mars_info_dict['hemi_image_urls'] = hemi_image_urls
  print(mars_info_dict['hemi_image_urls'])
  
  browser.quit()
  return mars_info_dict



