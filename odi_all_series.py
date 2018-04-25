# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:12:57 2018

@author: Vasthav
"""

import requests
import re
from bs4 import BeautifulSoup


if __name__ == '__main__':
    url = "http://stats.espncricinfo.com/ci/content/records/335432.html"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    winner_arr = ["Australia", "India", "Bangladesh", "West Indies", "Sri Lanka", "Pakistan", "South Africa", "New Zealand", "England", "Zimbabwe"]
    #countries_data = soup.find_all('select', attrs={'name': re.compile("cboCountry1")})
    #options = countries_data[0].find_all('option')
    all_rows = soup.find_all('tr', attrs={'class': re.compile("data1")})
    #print(all_rows)
    count = 0
    for row in all_rows:
        series_margin = ""
        href = row.find_all('a', attrs={'href': re.compile("/")})
        margin = row.find_all('td', attrs={'nowrap': re.compile("nowrap")})
        winner = row.find_all('a', attrs={'href': re.compile("/ci/content/team")})
        series_margin = margin[3].text
        winner = winner[0].text.strip()
        if series_margin == "":
            #count = count + 1
            if winner in winner_arr:
                print(winner)
                count = count + 1
                host_nation_arr = href[0].text.strip()
                if "(" in host_nation_arr:
                    host_nation_arr = host_nation_arr.split("(")
                    #print(host_nation_arr[1])
                    host_nation = host_nation_arr[1].split("in")
                    #count = count + 1
                    if len(host_nation) > 1:
                        host_nation = host_nation[1].strip(")")
                        #print(host_nation.strip())
                    else:
                        print("")
                        #print(host_nation)
                elif "in" in host_nation_arr:
                    host_nation_arr = host_nation_arr.split("in")
                    #print(host_nation_arr[1])
                    #count = count + 1
                else:
                    print("hi-1")
    print(count)