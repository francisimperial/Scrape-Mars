from bs4 import BeautifulSoup as bs
import numpy as numpy
import pandas as pd 
import requests 

def scrape():
    # scrape NASA Mars News Site for title, paragraph text
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="rollover_description_inner").text

    # get latest Mars Weather Info
    url="https://twitter.com/marswxreport?lang=en"
    response=requests.get(url)
    soup = bs(response.text, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    # find fun facts about Mars
    url="https://space-facts.com/mars/"
    response=requests.get(url)
    table = pd.read_html(url)
    df_mars_facts = pd.DataFrame(table[0])
    df_mars_facts.columns=["Parameters","Values"]
    df_mars_facts.set_index(["Parameters"])
    html_table_string = df_mars_facts.to_html()

    # create list of dictionaries of images and urls
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response=requests.get(url)
    soup=bs(response.text, "html.parser")
    hemi_result_list = soup.find_all("div", class_="item")
    hemi_dict_list = []
    for result in hemi_result_list:
        # find image title
        img_title = result.find("h3").text
        # find image url
        to_image = "https://astrogeology.usgs.gov/" + result.find("a", class_="itemLink product-item")["href"]
        image_response = requests.get(to_image)
        soup = bs(image_response.text, "html.parser")
        img_url = soup.find("div", class_="downloads").find("a")["href"]
        hemi_dict_list.append({"title":img_title, "img_url":img_url})

    # create dictionary of all the information
    mars_library = {
        "News_Title": news_title,
        "Paragraph_Text": news_p,
        "Mars_Weather": mars_weather,
        "Mars_Facts":html_table_string,
        "Mars_Hemispheres": hemi_dict_list
    }

    return mars_library