# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': '/opt/homebrew/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)   

    

# Set the executable path and initialize the chrome browser in splinter (this was from earlier in module)
#executable_path = {'executable_path': '/opt/homebrew/bin/chromedriver'}
#browser = Browser('chrome', **executable_path, headless=False)   

def mars_news(browser):
    # Scrape Mars news
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except block for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError: 
        return None, None
    
    return news_title, news_p


# ## Featured Images

def featured_image(browser):

    # visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

        # Use the base URL to create an absolute URL
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url


    # ## Mars Facts
def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
   
   except: BaseException 
        return None
    
    # Assign columns and set index of DataFrames
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert DataFrame into html format, add bootstrap
    return df.to_html()

browser.quit()




