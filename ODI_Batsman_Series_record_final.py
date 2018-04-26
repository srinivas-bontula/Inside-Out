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
import pandas as pd

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
    
    
def get_series_data(decades_tuple,series_wise_matches,cricket_url):
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
        record_string = record_string + get_details(appended_url, series_num,country_arr,decades_tuple,series_wise_matches)
    #print_in_csv(record_string)    
    return record_string 
    
def get_series_data_code(decades_tuple, df, series_wise_matches, series_code):
    #elements = []  
    record_string=""
    #series_code = "0779"       
    url = 'http://www.howstat.com/cricket/Statistics/Series/SeriesStats_ODI.asp?SeriesCode='+str(series_code)
    #print(url)
    '''page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    odi_series = soup.find_all('tr', attrs={'bgcolor': re.compile("#")})'''
    country_arr = []
    if int(series_code) in df.index:
        country = df["Series Country"][int(series_code)]
        if "," in country:
            y = country.split(",")
            for i in y:
                country_arr.append(i.strip())
        else:
            country_arr.append(country.strip())
        appended_url = url + '&Scope=All#bat'
        appended_url = appended_url.replace("SeriesStats_ODI.asp", "SeriesAnalysis_ODI.asp")
        #series_url = 'http://www.howstat.com/cricket/Statistics/Series/' + series_code + '&Scope=All#bat'
        #country_name = 
        record_string = record_string + get_details(appended_url, series_code,country_arr,decades_tuple, series_wise_matches)
        #print_in_csv(record_string)
        return record_string
    else:
        return ""
    #elements = odi_series[0].find_all('td')
    #print(elements[2].text)
    '''for row in odi_series:
        elements = row.find_all('td')
        location = elements[2].text
        location = location.split(",")[-1].strip()
        #print(location)
        count = 0
        country = country_location(location,count)
        #print(location, "->", country)
        if (country not in country_arr) and country != '':
            country_arr.append(country)
        print (country)
    #country_arr.replace("United Kingdom", "England") 
    for index, item in enumerate(country_arr):
        if item == "UK":
            country_arr[index] = "England"
        elif item not in country_names:
            country_arr.pop(index)
    print(country_arr)'''
    

'''def country_location(city,count): 
    geolocator = Nominatim()
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
    return
    #print(city)
    #sleep(1)
    g = geocoder.google(city)
    total_addr = g.address
    if not total_addr:
        if count != 5:
            sleep(0.1)
            count+=1
            country_location(city,count)
        else:
            return "" 
    else:    
        country = total_addr.split(",")[-1].strip()
        return country'''
       
    
def get_details(appended_url, series_num,country_name,decades_tuple,series_wise_matches):
    #page = requests.get(appended_url)
    #### to add the column decade in the csv ####
    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index[0]
    matches_index = decades_tuple[decade_val].index(series_num)
    matches_in_ser = series_wise_matches[decade_val][matches_index]
    #print(matches_index)
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
            record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) +"," + str(matches_in_ser) + "\n"
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
    series_wise_matches = ()
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
        series_list_filtered, nbs_codes, series_matches = all_series_of_decade(url)
        decade_wise_series = decade_wise_series + (series_list_filtered,)
        series_wise_matches = series_wise_matches + (series_matches,)
        non_bilateral.append(nbs_codes)
    non_bilateral = [item for sublist in non_bilateral for item in sublist]
    #print(len(flat_list))
    return decade_wise_series, non_bilateral, series_wise_matches
        
        
        
def all_series_of_decade(url):
    odi_matches = ()
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
    #for x in series_codes:

    for tr in odi_series:                                                             
        series_codes = tr.find_all('td')[0]
        link = series_codes.find('a', attrs={'class': re.compile("LinkNormal")})
        series_url = link.get('href')
        series_url = series_url.split("=")
        series_url = series_url[1]
        odi_series_code = odi_series_code + (series_url,)
        #print(odi_series_code)
        series_matches = tr.find_all('td')[2]
        #for x in series_codes:
        link = series_matches.text.strip()
        odi_matches = odi_matches + (link,)
        #series_url = link.get('href')
        #series_url = series_url.split("=")
        #series_url = series_url[1]
        #odi_series_code = odi_series_code + (series_url,)     
        #print(link)
        result = tr.find_all('td')[3]
        #for i in result:
        t = result.text.strip()
        if "-" not in t and t != "":
            if t in country_names:
                #print(t)
                non_bilateral_series.append(odi_series_code[count])
        count += 1
        #print(non_bilateral_series)
    #print(len(non_bilateral_series))
    return odi_series_code, non_bilateral_series, odi_matches    
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
    decades_tuple, non_bilateral, series_wise_matches = get_series_with_decades(series_url)
    #print(len(series_wise_matches))
    #print(series_wise_matches)
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
    
    df = pd.read_csv("Series_code_to_country.csv", index_col = 0)
    
    #cricket_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry.asp?A=AUS&B=BAN&W=X"
    #print(all_series_list)
    
    download_dir = "records_final_series_odi_v10.csv" #where you want the file to be downloaded to 
    file = open(download_dir, "a") 
    header = "Player,Country,% Team Runs,Mat,Inns,NO,50s,100s,0s,HS,Runs,S/R,Avg,Ca,St,Series_Code, H/A, Decade_Index ,Matches\n"
    file.write(header)
    '''for snl_link in all_series_list[:1]:
        threads.append(threading.Thread(target=get_series_data, args=(snl_link,)))'''
        
    '''for code in non_bilateral[:1]:
        threads.append(threading.Thread(target=get_series_data_code, args=(decades_tuple,code,)))
        
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()'''
    get_series_data_with_decades_list = partial(get_series_data,decades_tuple,series_wise_matches)
    
    
    with Pool(45) as p:
        records = p.map(get_series_data_with_decades_list,all_series_list)
        p.terminate()
        p.join()
    
    print_in_csv(records)
    
    get_series_data_with_decades_list_code = partial(get_series_data_code,decades_tuple,df,series_wise_matches)
    
    with Pool(80) as p:
        records = p.map(get_series_data_with_decades_list_code,non_bilateral)
        p.terminate()
        p.join()

    print_in_csv(records) 
    
    file.close()
    #print_in_csv(series_list) 
    
