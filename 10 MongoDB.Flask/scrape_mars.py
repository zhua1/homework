# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


# Put everything into a function
def scrape():
    
    # Initialize dict to append all needed data
    d = {}
    
    words = requests.get('https://mars.nasa.gov/news').text
    data = re.split("<a href='/news/", words)[1]
    title = re.split("'", re.split("</div>\n<img alt='", data)[1])[0]
    paragraph = re.split(" \n</div>\n<div class='overlay_arrow'>", re.split("<div class='rollover_description_inner'>\n", data)[1])[0]
    if "&quot;" in paragraph:
        paragraph = re.sub("&quot;", r'"', paragraph)
    img = re.split("-", re.split("_", re.split("' src=", re.split("/system/news_items/list_view_images/", data)[1])[0])[1])[0]
    image_url = f'https://www.jpl.nasa.gov/spaceimages/images/largesize/{img}_hires.jpg'
    
    weather = requests.get('https://twitter.com/marswxreport').text
    
    mar_weather = 'Sol' + re.split('</p>\n</div>', weather.split('<p class="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text" lang="en" data-aria-label-part="0">Sol')[1])[0]
    
    if "&quot;" in mar_weather:
        mar_weather = re.sub("&quot;", r'"', mar_weather)
    
    
    # Get Mars Facts
    facts = requests.get('https://space-facts.com/mars/').text
    
    facts_dict = {}
    names = ['Equatorial Diameter', 'Polar Diameter', 'Mass', 'Moons', 'Orbit Distance', 'Orbit Period', 'Surface Temperature', 'First Record', 'Recorded By']
    
    for name in names:
        try:
            facts_dict[name] = re.split('<br />', facts.split(name+':</strong></td><td class="column-2">')[1])[0]
        except IndexError:
            facts_dict[name] = re.split('<br />', facts.split(name+': </strong></td><td class="column-2">')[1])[0]
        if '</td>' in facts_dict[name]:
            facts_dict[name] = re.split('</td>', facts_dict[name])[0]
        if '<a href=' in facts_dict[name]:
            facts_dict[name] = BeautifulSoup(facts_dict[name], 'html.parser')
            for a in facts_dict[name].findAll('a'):
                del a['href']
            facts_dict[name] = str(facts_dict[name])
        if '<a>' in facts_dict[name]:
            facts_dict[name] = facts_dict[name].replace('<a>', '')
        if '</a>' in facts_dict[name]:
            facts_dict[name] = facts_dict[name].replace('</a>', '')
        if '&amp;' in facts_dict[name]:
            facts_dict[name] = facts_dict[name].replace('&amp;', '&')
    
    df = pd.DataFrame.from_dict(facts_dict, orient='index')
    df.columns = ['Value']
    html_table = df.to_html(border = '1', justify = 'center')
    
    spheres = ['valles_marineris', 'cerberus', 'schiaparelli', 'syrtis_major']
    titles = ['Valles Marineris Hemisphere', 'Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere']
    
    hemisphere_image_urls = []
    for i in range(len(spheres)):
        dic = {}
        dic['title'] = titles[i]
        dic['img_url'] = f'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{spheres[i]}_enhanced.tif/full.jpg'
        hemisphere_image_urls.append(dic)
    
    # Append title, paragraph, mar_weather, image_url, html_table    
    d['title'] = title
    d['paragraph'] = paragraph
    d['mar_weather'] = mar_weather
    d['image_url'] = image_url
    d['html_table'] = html_table
    d['hemisphere_image_urls'] = hemisphere_image_urls
    
    return(d)
    
    
    
    
    
    
    
    