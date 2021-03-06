
import requests
import re
from bs4 import BeautifulSoup
#import time
import random
import itertools as it
import threading

def get_all_countries(url):
    countries_list = []
    
    url = url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    countries_data = soup.find_all('select', attrs={'name': re.compile("cboCountry1")})
    options = countries_data[0].find_all('option')

    for data in options:
        country = data.get('value')
        countries_list.append(country)

    return countries_list
    
    
def get_series_data(cricket_url):
    record_string = ""
    
    url = cricket_url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    possible_links = soup.find_all('a', attrs={'href': re.compile("SeriesStats.asp")})

    for link in possible_links:
        series_code = str(link.get('href'))
        country = link.text.strip()
        country_name_arr = country.split(" ")
        country_name = country_name_arr[1]
        if country_name_arr[2] != 'v.':
            country_name = country_name + ' ' +country_name_arr[2]
        series_url = 'http://www.howstat.com/cricket/Statistics/Series/' + series_code
        appended_url = series_url + '&Scope=All#bat'
        appended_url = appended_url.replace("SeriesStats.asp", "SeriesAnalysis.asp")
        record_string = record_string + get_details(appended_url, series_code,country_name)
        
    print_in_csv(record_string)    
    
        
        
def get_details(appended_url, series_code,country_name):

    code = series_code.split("=")
    series_num = code[1].strip()

    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index [0]

    page1 = requests.get(appended_url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    batting_records = soup.find('div', attrs={'id': re.compile("bat")})
    tables = batting_records.find_all('tr', attrs={'bgcolor': re.compile("#")})

    record_string = ""
    for table in tables:
        name= table.find_all('td', attrs={'align': re.compile("left")})
        tdTags = table.find_all('td', attrs={'align': re.compile("right")})
        count = 0
        for tdTag in name:
            name = tdTag.text.strip()
            if count==0:
                name = name.replace(",","")
                count += 1
            elif count==1:
                if name == country_name:
                    H_A = "Home"
                else:
                    H_A = "Away"
                count += 1    
            record_string = record_string + name + "," 
            
        
        for tdTag in tdTags:
            record_string = record_string + tdTag.text.strip() + ","
            
        record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) + "\n"
    return record_string
    
def print_in_csv(records):
    for line in records:
        file.write(line)

def get_series_with_decades(url):
    decade_wise_series = ()
    
    url = url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    test_series = soup.find('div', attrs={'id': re.compile("tests")})
    possible_links = test_series.find_all('a', attrs={'class': re.compile("LinkOff")})
    
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/"
    for link in possible_links:
        series_decade_url = partial_url + link.get('href')
        url = series_decade_url.strip()
        series_list_filtered = all_series_of_decade(url)
        decade_wise_series = decade_wise_series + (series_list_filtered,)
    return decade_wise_series
        
        
        
def all_series_of_decade(url):
    test_series_code = ()
    
    url = url.strip()
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

    countries_list = get_all_countries(series_url)
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?"
    for country1,country2 in list(it.combinations(countries_list,2)):
        list_series_url = partial_url + "A=" + country1 +"&B=" + country2  
        all_series_list.append(list_series_url)

    download_dir = "test_batsman_records_1.csv" #where you want the file to be downloaded to 
    file = open(download_dir, "a") 
    header = "Player,Country,% Team Runs,Mat,Inns,NO,50s,100s,0s,HS,Runs,S/R,Avg,Ca,St,Series_Code, H/A, Decade_Index \n"
    file.write(header)
    for snl_link in all_series_list:
        threads.append(threading.Thread(target=get_series_data, args=(snl_link,)))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    file.close()

    
