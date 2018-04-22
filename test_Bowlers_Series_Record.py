# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 22:37:41 2018

@author: Vasthav
"""

import requests
import re
from bs4 import BeautifulSoup
#import time
#import random
import itertools as it
import threading

final_list = []
download_dir = "records_final_series_test_final_bowlers_v6.csv"
#records = []

proxies = {}


def get_all_countries(url):
    #print(decades_tuple)
    countries_list = []
    url = url.strip()
    #proxies['http'] = random.choice(proxies_list)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    countries_data = soup.find_all('select', attrs={'name': re.compile("cboCountry1")})
    options = countries_data[0].find_all('option')
    #print(options)
    for data in options:
        country = data.get('value')
        #print(country)
        countries_list.append(country)
    #print(countries_data.option)
    return countries_list
    
    
def get_series_data(cricket_url):
    url = cricket_url.strip()
    
    #print(proxies)
    #page = requests.get(url, proxies=proxies)
    #proxies['http'] = random.choice(proxies_list)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    possible_links = soup.find_all('a', attrs={'href': re.compile("SeriesStats.asp")})
    #print(possible_links)
    record_string = ""
    for link in possible_links:
        #print(link)
        series_code = str(link.get('href'))
        country = link.text.strip()
        #country_name = country.split(" ")[1]
        country_name_arr = country.split(" ")
        country_name = country_name_arr[1]
        if country_name_arr[2] != 'v.':
            country_name = country_name + ' ' +country_name_arr[2]
        #print(series_code)
        #print(country_name)
        series_url = 'http://www.howstat.com/cricket/Statistics/Series/' + series_code
        appended_url = series_url + '&Scope=All#bowl'
        appended_url = appended_url.replace("SeriesStats.asp", "SeriesAnalysis.asp")
        #print(appended_url)
        record_string = record_string + get_details(appended_url, series_code,country_name)
    print_in_csv(record_string)    
    
        
        
def get_details(appended_url, series_code,country_name):
    #page = requests.get(appended_url)
    code = series_code.split("=")
    series_num = code[1].strip()
    #### to add the column decade in the csv ####
    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index [0]
    #proxies['http'] = random.choice(proxies_list)
    #page1 = requests.get(appended_url,proxies=proxies)
    page1 = requests.get(appended_url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    #print(soup)
    batting_records = soup.find('div', attrs={'id': re.compile("bowl")})
    tables = batting_records.find_all('tr', attrs={'bgcolor': re.compile("#")})
    #table = div.find_all('table', attrs={'id': re.compile("TableLined")})
    #print(div.table)
    #print(tables)
    record_string = ""
    for table in tables:
        
        #print(table)
        name= table.find_all('td', attrs={'align': re.compile("left")})
        #print(name)
        tdTags = table.find_all('td', attrs={'align': re.compile("right")})
        count = 0
        for tdTag in name:
            name = tdTag.text.strip()
            if count==0:
                name = name.replace(",","")
                count += 1
            elif count==1:
                #print(name)
                if name == country_name:
                    H_A = "Home"
                else:
                    H_A = "Away"
                count += 1    
            #print(tdTag.text)
            
            #print(name)
            #record.append(tdTag.text.strip())
            #print(tdTag.text)
            record_string = record_string + name + "," 
            
        
        for tdTag in tdTags:
            tdTag = tdTag.text.strip()
            #print(tdTag)
            #print(tdTag.text)
            #record.append(tdTag.text.strip())
            if "/" in tdTag:
                tdTag = tdTag.replace("/","|")
                print(tdTag)
                
            record_string = record_string + tdTag + ","
        
        #record_string.strip(-1)
        record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) + "\n"
        #print(record_string)
        #print_in_csv(record_string)
    #print(record_string)
    return record_string
    #print_in_csv(record_string)
        
        #print(tdTags1.text)
        #print(tdTags.text)
        
            #print(tdTags.text)
        #tdTags1 = table.find_all('td', attrs={'class': re.compile("align-left")})
        #tdTags1 = table.find_all('td')
        #if (tdTags1!=None):
           # print((tdTags1.text))
    #print(table.text)
    
    #print(title_box)
    
def print_in_csv(records):
    #filename = str(filename)
    file = open(download_dir, "a")
    for line in records:
        file.write(line)
    file.close()

def get_series_with_decades(url):
    decade_wise_series = ()
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/"
    url = url.strip()
    #proxies['http'] = random.choice(proxies_list)
    #print(proxies)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    test_series = soup.find('div', attrs={'id': re.compile("tests")})
    possible_links = test_series.find_all('a', attrs={'class': re.compile("LinkOff")})
    for link in possible_links:
        series_decade_url = partial_url + link.get('href')
        url = series_decade_url.strip()
        series_list_filtered = all_series_of_decade(url)
        decade_wise_series = decade_wise_series + (series_list_filtered,)
    return decade_wise_series
        
        
        
def all_series_of_decade(url):
    test_series_code = ()
    url = url.strip()
    #proxies['http'] = random.choice(proxies_list)
    #print(proxies)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    test_series = soup.find_all('a', attrs={'class': re.compile("LinkNormal")})
    for link in test_series:
        series_url = link.get('href')
        series_url = series_url.split("=")
        series_url = series_url[1]
        test_series_code = test_series_code + (series_url,)
    
    return test_series_code
       
    
    

if __name__ == '__main__':
    all_series_list = []
    threads = []
    series_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListMenu.asp#tests"
    decades_tuple = get_series_with_decades(series_url)
    #print(decades_tuple)
    #print(len(decades_tuple[0]))
    countries_list = get_all_countries(series_url)
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?"
    #print(countries_list)
    for country1,country2 in list(it.combinations(countries_list,2)):
        list_series_url = partial_url + "A=" + country1 +"&B=" + country2  
        all_series_list.append(list_series_url)
    #cricket_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?A=AUS&B=BAN&W=X"
    #print(all_series_list)
     #where you want the file to be downloaded to 
    header = "Player,Country,Mat,Overs,Maidens,Runs,Wickets,Best,5w,10w,Avg,S/R,E/R,Series_Code,H/A,Decade_Index\n"
    file = open(download_dir, "a")
    file.write(header)
    file.close()
    for snl_link in all_series_list:
        threads.append(threading.Thread(target=get_series_data, args=(snl_link,)))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    '''for snl_link in all_series_list:
        get_series_data(snl_link)'''
    
    #print_in_csv(series_list)
    
