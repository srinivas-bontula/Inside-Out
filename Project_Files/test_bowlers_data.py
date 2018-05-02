import requests
import re
from bs4 import BeautifulSoup
import itertools as it
import threading
from functools import partial
from multiprocessing.pool import Pool

final_list = []
download_dir = "test_bowlers_records_1.csv"


def get_all_countries(url):
    #returns all the test playing country codes and names 
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
    

def get_series_data(decades_tuple, cricket_url):
    # This function gets all the series data for a given pair of countries
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
        appended_url = series_url + '&Scope=All#bowl'
        appended_url = appended_url.replace("SeriesStats.asp", "SeriesAnalysis.asp")
        record_string = record_string + get_details(appended_url, series_code,country_name, decades_tuple)
    
    return record_string   
    
def get_details(appended_url, series_code,country_name, decades_tuple):
    #returns the players statistics for a particular series given the series_code 
    record_string = ""
    
    code = series_code.split("=")
    series_num = code[1].strip()
    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index [0]

    page1 = requests.get(appended_url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    batting_records = soup.find('div', attrs={'id': re.compile("bowl")})
    tables = batting_records.find_all('tr', attrs={'bgcolor': re.compile("#")})

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
            tdTag = tdTag.text.strip()
            
            if "/" in tdTag:
                tdTag = tdTag.replace("/","|")
                
            record_string = record_string + tdTag + ","
        record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) + "\n"
        
    return record_string

def print_in_csv(records):
    #prints all the records into the csv file 
    for line in records:
        if not line:
            file.write(line)

def get_series_with_decades(url):
    #return the groups of series codes into decades
    decade_wise_series = ()
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/"
    
    url = url.strip()
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
    # returns the tuple of the series codes given the url for a decade
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
        
    header = "Player,Country,Mat,Overs,Maidens,Runs,Wickets,Best,5w,10w,Avg,S/R,E/R,Series_Code,H/A,Decade_Index\n"
    file = open(download_dir, "a")
    file.write(header)
    for bilateral_link in all_series_list:
        threads.append(threading.Thread(target=get_series_data, args=(bilateral_link,)))
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    file.close()
    
