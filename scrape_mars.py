# import the dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import mars_urls as mars
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:\chromedrv\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

# Scrape the latest news headline from the NASA Mars Mission
# Path to results working as of May 15, 2019

def scrape_news_article(nasa_url=mars.NASA_URL, nasa_news_url=mars.NASA_NEWS_URL):
    """
    Args:  The URL for the NASA Mars Mission and the URL for the news section.
    Returns the title and first paragraph for the most recent article in the latest news.
    """
    # Initialize and move the browser to the URL
    browser = init_browser()
    browser.visit(nasa_news_url)
    
    # retrieve html and pass to Beautiful Soup for parsing
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # from the main page we can get teaser titles and bodies
    titles = soup.find_all('div', class_="content_title")
    first_story = titles[0]
    first_story_title = first_story.get_text()
    first_story_anchor = first_story.find('a', target="_self")
    first_story_url = first_story_anchor.get('href')
    
    # short story body from the main page:
    bodies = soup.find_all('div', class_='article_teaser_body')
    first_body = bodies[0]
    first_story_oneliner = first_body.get_text()
    
    # Now move the broswer to the full story page and grab the first paragraph.
    first_story_url = nasa_url + first_story_url
    browser.visit(first_story_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    titles = soup.find_all('h1', class_="article_title")
    first_title = titles[0].get_text().strip()
    
    first_paragraph = soup.find_all('p')[0].get_text()
    
    return first_story_title, first_story_oneliner, first_paragraph

# Scrape the latest featured image from the JPL Mars page
# Path to results working as of May 15, 2019

def scrape_jpl_featured_image(jpl_url=mars.JPL_URL, jpl_mars_url=mars.JPL_MARS_URL):
    """
    Return URL for the current day's featured Mars image.  The input args are the 
    current URLs to the JPL and the JPL's featured Mars image of the day.
    """
    
    # initialize browser
    browser = init_browser()

    # visit the main Mars featured image site.
    browser.visit(jpl_mars_url)
    
    # grab the html and pass to BeautifulSoup for parsing
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, "html.parser")
    
    # As of May 14, 2019, one way to grab the featured image URL is the following:
    # We can find the link to the story for the background image
    story_anchor = jpl_soup.find_all('a', class_="button fancybox")[0] 
    story_url = story_anchor.get('data-link')
    story_url = jpl_url + story_url
    #print(story_url)
    
    # now move the browser to the story page
    browser.visit(story_url)
    story_html = browser.html
    story_soup = BeautifulSoup(story_html, "html.parser")
    
    # on the story page, there is a URL to the full-size image
    full_image_anchor = story_soup.find_all('img', class_="main_image")[0] 
    full_image_url = full_image_anchor.get('src')
    
    return jpl_url + full_image_url

def scrape_mars_facts(mars_facts_url = mars.MARS_FACTS_URL):
    """
    """
    tables = pd.read_html(mars_facts_url)
    mars_df = tables[1] # this needed to be changed from 0 - should be a more robust way to get this information
    mars_df.columns = ["description", "value"]
    mars_df.set_index("description", inplace=True)
    
    return mars_df.to_html()

# Scrape the four hemisphere image titles and urls

def scrape_mars_hemispheres(usgs_url=mars.MARS_USGS, hemispheres_url=mars.MARS_HEMISPHERES):
    """
    Return URL for the current day's featured Mars image.  The input args are the 
    current URLs to the JPL and the JPL's featured Mars image of the day.
    """
    
    # initialize browser
    browser = init_browser()

    # visit the Mars hemispheres site.
    browser.visit(hemispheres_url)
    
    # Now search for each hemisphere name in a link
    # A list of hemisphere names
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis Major", "Valles Marineris"]

    hemisphere_image_urls = []
    
    for hemisphere in hemispheres:
        title = browser.find_link_by_partial_text(hemisphere).first.text
        browser.click_link_by_partial_text(hemisphere)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        suburl = soup.find_all('img', class_="wide-image")[0].get('src')
        img_url = usgs_url + suburl
        
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        browser.back()
        
    return hemisphere_image_urls

# Scrape the Mars weather twitter timeline

def scrape_mars_weather(weather_url=mars.MARS_WEATHER):
    """
    Return the first item in the Mars weather twitter timeline that is a weather item.
    """
    # First - a helper function:
    def match_weather_tweet(tweet):
        "If a weather tweet return it or return False."
        if tweet.find('InSight sol') == 0:
            start = tweet.find('InSight sol')
            end = tweet.find('pic.twitter.com')
            return tweet[start:end]
        else:
            return False
   
    browser = init_browser()
    browser.visit(weather_url)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    # grab each tweet from the timeline - includes retweets
    timeline = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # alternate - but requires additional parsing...
    # timeline = soup.find_all('li', class_="stream-item")
    
    # create a list of tweets strings from the timeline 
    timeline_text = [match_weather_tweet(tweet.get_text()) for tweet in timeline]
    
    return next(tweet for tweet in timeline_text)

def scrape():
    """
    Returns a dictionary of items scraped using the various functions above.
    """
    
    # grab the news article
    news_title, news_p, news_longp = scrape_news_article()
    
    # grab the JPL image
    featured_image_url = scrape_jpl_featured_image()
    
    # grab the weather tweet
    mars_weather = scrape_mars_weather()
    
    # grab the Mars facts:
    mars_facts = scrape_mars_facts()
    
    # grab the hemisphere image urls
    hemisphere_image_urls = scrape_mars_hemispheres()
    
    # prepare the dictionary for returning results:
    # note we could load the dict with the function calls above
    scrape_dict = {}
    scrape_dict['news_title'] = news_title
    scrape_dict['news_p'] = news_p
    scrape_dict['news_longp'] = news_longp
    scrape_dict['featured_image_url'] = featured_image_url
    scrape_dict['mars_weather'] = mars_weather
    scrape_dict['mars_facts'] = mars_facts
    scrape_dict['hemisphere_image_urls'] = hemisphere_image_urls
    
    return scrape_dict
