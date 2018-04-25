import requests
import re
from bs4 import BeautifulSoup
import itertools as it
import threading
from geopy.geocoders import Nominatim
from multiprocessing.pool import Pool
from functools import partial
from geopy.exc import GeocoderTimedOut
from time import sleep
import geocoder

final_list = []
#records = []
country_names=[]
decade_tuple=()


def get_all_countries(url):
    #print(decades_tuple)
    countries_list = []
    country_names = []
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
        country_name = data.text.strip()
        #print(country)
        countries_list.append(country)
        country_names.append(country_name)
    #print(countries_data.option)
    return countries_list,country_names
    
    
def get_series_data(decades_tuple,cricket_url):
    url = cricket_url.strip()
    
    #print(proxies)
    #page = requests.get(url, proxies=proxies)
    #proxies['http'] = random.choice(proxies_list)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    possible_links = soup.find_all('a', attrs={'href': re.compile("SeriesStats_ODI.asp")})
    #print(possible_links)
    record_string = ""
    #print(possible_links)
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
        code = series_code.split("=")
        series_num = code[1].strip()
        appended_url = series_url + '&Scope=All#bat'
        appended_url = appended_url.replace("SeriesStats_ODI.asp", "SeriesAnalysis_ODI.asp")
        #print(appended_url)
        country_arr = [country_name]
        record_string = record_string + get_details(appended_url, series_num,country_arr,decades_tuple)
    #print_in_csv(record_string)    
    return record_string 
    
def get_series_data_code(decades_tuple,series_code):
    elements = []  
    record_string=""
    #series_code = "0779"       
    url = 'http://www.howstat.com/cricket/Statistics/Series/SeriesStats_ODI.asp?SeriesCode='+str(series_code)
    #print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    odi_series = soup.find_all('tr', attrs={'bgcolor': re.compile("#")})
    country_arr = []
    #elements = odi_series[0].find_all('td')
    #print(elements[2].text)
    for row in odi_series:
        elements = row.find_all('td')
        location = elements[2].text
        location = location.split(",")[-1]
        #print(location)
        country = country_location(location)
        #print(location, "->", country)
        if country not in country_arr and country:
            country_arr.append(country)
    #country_arr.replace("United Kingdom", "England") 
    for index, item in enumerate(country_arr):
        if item == "United Kingdom":
            country_arr[index] = "England"

    #print(country_arr)
    appended_url = url + '&Scope=All#bat'
    appended_url = appended_url.replace("SeriesStats_ODI.asp", "SeriesAnalysis_ODI.asp")
    #series_url = 'http://www.howstat.com/cricket/Statistics/Series/' + series_code + '&Scope=All#bat'
    #country_name = 
    record_string = record_string + get_details(appended_url, series_code,country_arr,decades_tuple)
    #print_in_csv(record_string)
    return record_string
def country_location(city): 
    '''geolocator = Nominatim()
    try:
        print(city)
        sleep(0.1)
        location = geolocator.geocode(city,language="en")
        if location:
            total_addr = location.address
            country = total_addr.split(",")[-1].strip()
            return country
    except GeocoderTimedOut as e:
        print("Error: geocode failed on input %s with message %s"%(city, e))    
    return'''
    print(city)
    g = geocoder.google(city)
    total_addr = g.address
    if not total_addr:
        print(city)
    else:    
        country = total_addr.split(",")[-1].strip()
        return country
    return ""    
    
def get_details(appended_url, series_num,country_name,decades_tuple):
    #page = requests.get(appended_url)
    #### to add the column decade in the csv ####
    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index [0]
    #proxies['http'] = random.choice(proxies_list)
    #page1 = requests.get(appended_url,proxies=proxies)
    page1 = requests.get(appended_url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    #print(soup)
    #print(series_code)
    batting_records = []
    batting_records = soup.find('div', attrs={'id': re.compile("bat")})
    '''if batting_records.size:
        return'''
    record_string = ""
    if batting_records:    
        tables = batting_records.find_all('tr', attrs={'bgcolor': re.compile("#")})
        #table = div.find_all('table', attrs={'id': re.compile("TableLined")})
        #print(div.table)
        #print(tables)
        
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
                    if name in country_name:
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
                #print(tdTag.text)
                #record.append(tdTag.text.strip())
                record_string = record_string + tdTag.text.strip() + ","
            
            #record_string.strip(-1)
            record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) + "\n"
            #print(record_string)
            #print_in_csv(record_string)
        #print(record_string)
        
    
    return record_string
        
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
    for line in records:
        if line:
            file.write(line)
    #file.close()

def get_series_with_decades(url):
    decade_wise_series = ()
    non_bilateral = []
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/"
    url = url.strip()
    #proxies['http'] = random.choice(proxies_list)
    #print(proxies)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    odi_series = soup.find('div', attrs={'id': re.compile("odis")})
    possible_links = odi_series.find_all('a', attrs={'class': re.compile("LinkOff")})
    for link in possible_links:
        series_decade_url = partial_url + link.get('href')
        url = series_decade_url.strip()
        series_list_filtered, nbs_codes = all_series_of_decade(url)
        decade_wise_series = decade_wise_series + (series_list_filtered,)
        non_bilateral.append(nbs_codes)
    non_bilateral = [item for sublist in non_bilateral for item in sublist]
    #print(len(flat_list))
    return decade_wise_series, non_bilateral
        
        
        
def all_series_of_decade(url):
    odi_series_code = ()
    non_bilateral_series = []
    url = url.strip()
    #proxies['http'] = random.choice(proxies_list)
    #print(proxies)
    #page = requests.get(url,proxies=proxies)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #odi_series = soup.find_all('a', attrs={'class': re.compile("LinkNormal")})
    odi_series = soup.find_all('tr', attrs={'bgcolor': re.compile("#")})
    count = 0
    for tr in odi_series:                                                             
        series_codes = tr.find_all('td')[::4]
        for x in series_codes:
            link = x.find('a', attrs={'class': re.compile("LinkNormal")})
            series_url = link.get('href')
            series_url = series_url.split("=")
            series_url = series_url[1]
            odi_series_code = odi_series_code + (series_url,)
            
        result = tr.find_all('td')[3::4]
        for i in result:
            t = i.text.strip()
            if "-" not in t and t != "":
                if t in country_names:
                    non_bilateral_series.append(odi_series_code[count])
            count += 1

    return odi_series_code, non_bilateral_series     
    '''for link in odi_series:
        series_url = link.get('href')
        series_url = series_url.split("=")
        series_url = series_url[1]
        odi_series_code = odi_series_code + (series_url,)
    
    return odi_series_code'''
       
    
    

if __name__ == '__main__':
    all_series_list = []
    threads = []
    series_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListMenu.asp#odis"
    #global country_names, decades_tuple, non_bilateral
    countries_list, country_names = get_all_countries(series_url)
    #print(country_names)
    decades_tuple, non_bilateral = get_series_with_decades(series_url)
    #print(decades_tuple)
    #print(non_bilateral)
    #print(decades_tuple)
    #print(len(non_bilateral))
    #print(len(decades_tuple[0]))
    #countries_list = get_all_countries(series_url)
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry_ODI.asp?"
    #print(countries_list)
    for country1,country2 in list(it.combinations(countries_list,2)):
        list_series_url = partial_url + "A=" + country1 +"&B=" + country2  
        all_series_list.append(list_series_url)        
    #cricket_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?A=AUS&B=BAN&W=X"
    #print(all_series_list)
    
    download_dir = "records_final_series_odi_v5.csv" #where you want the file to be downloaded to 
    file = open(download_dir, "a") 
    header = "Player,Country,% Team Runs,Mat,Inns,NO,50s,100s,0s,HS,Runs,S/R,Avg,Ca,St,Series_Code, H/A, Decade_Index \n"
    file.write(header)
    '''for snl_link in all_series_list[:1]:
        threads.append(threading.Thread(target=get_series_data, args=(snl_link,)))'''
        
    '''for code in non_bilateral:
        threads.append(threading.Thread(target=get_series_data_code, args=(code,)))
        
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()'''
    '''get_series_data_with_decades_list = partial(get_series_data,decades_tuple)
    
    
    with Pool(45) as p:
        records = p.map(get_series_data_with_decades_list,all_series_list)
        p.terminate()
        p.join()
    
    print_in_csv(records)    '''
    
    get_series_data_with_decades_list_code = partial(get_series_data_code,decades_tuple)
    
    with Pool(80) as p:
        records = p.map(get_series_data_with_decades_list_code,non_bilateral)
        p.terminate()
        p.join() 

    print_in_csv(records)   
    
    file.close()
    #print_in_csv(series_list) '''
    
