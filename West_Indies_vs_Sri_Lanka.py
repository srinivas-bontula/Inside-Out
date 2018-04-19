# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 00:42:59 2018

@author: Vasthav
"""

import requests
import re
from bs4 import BeautifulSoup
series_url = 'http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?A=WIN&B=SRL&W=X'
page = requests.get(series_url)
soup = BeautifulSoup(page.content, 'html.parser')
possible_links = soup.find_all('a', attrs={'href': re.compile("SeriesStats.asp")})
    #print(possible_links)
record_string = ""
for link in possible_links:
        #print(link)
    series_code = str(link.get('href'))
    country = link.text.strip()
    country_name_arr = country.split(" ")
    country_str = country_name_arr[1]
    if country_name_arr[2] != 'v.':
        country_str = country_str + ' ' +country_name_arr[2] 
    print(country_str)
    
    