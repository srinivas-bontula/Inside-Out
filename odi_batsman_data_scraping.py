import requests
import re
from bs4 import BeautifulSoup
import itertools as it
from multiprocessing.pool import Pool
from functools import partial
import pandas as pd

def get_all_countries(url):
    countries_list = []
    country_names = []
    
    url = url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    countries_data = soup.find_all('select', attrs={'name': re.compile("cboCountry1")})
    options = countries_data[0].find_all('option')
    
    for data in options:
        country = data.get('value')
        country_name = data.text.strip()
        countries_list.append(country)
        country_names.append(country_name)
        
    return countries_list,country_names
    
    
def get_series_data(decades_tuple,series_wise_matches,cricket_url):
    
    url = cricket_url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    possible_links = soup.find_all('a', attrs={'href': re.compile("SeriesStats_ODI.asp")})

    record_string = ""
    for link in possible_links:
        
        country = link.text.strip()
        country_name_arr = country.split(" ")
        country_name = country_name_arr[1]
        if country_name_arr[2] != 'v.':
            country_name = country_name + ' ' +country_name_arr[2]

        series_code = str(link.get('href'))
        series_url = 'http://www.howstat.com/cricket/Statistics/Series/' + series_code
        code = series_code.split("=")
        series_num = code[1].strip()
        
        appended_url = series_url + '&Scope=All#bat'
        appended_url = appended_url.replace("SeriesStats_ODI.asp", "SeriesAnalysis_ODI.asp")
        country_arr = [country_name]
        record_string = record_string + get_details(appended_url, series_num,country_arr,decades_tuple,series_wise_matches)   
    return record_string 
    
def get_series_data_code(decades_tuple, df, series_wise_matches, series_code):
 
    record_string=""     
    url = 'http://www.howstat.com/cricket/Statistics/Series/SeriesStats_ODI.asp?SeriesCode='+str(series_code)
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
        record_string = record_string + get_details(appended_url, series_code,country_arr,decades_tuple, series_wise_matches)
        return record_string
    else:
        return ""
       
    
def get_details(appended_url, series_num,country_name,decades_tuple,series_wise_matches):

    decade_index = [decades_tuple.index(item) for item in decades_tuple if series_num in item]
    decade_val = decade_index[0]
    matches_index = decades_tuple[decade_val].index(series_num)
    matches_in_ser = series_wise_matches[decade_val][matches_index]

    page1 = requests.get(appended_url)
    soup = BeautifulSoup(page1.content, 'html.parser')
    batting_records = []
    batting_records = soup.find('div', attrs={'id': re.compile("bat")})

    record_string = ""
    if batting_records:    
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
                    if name in country_name:
                        H_A = "Home"
                    else:
                        H_A = "Away"
                    count += 1    
                record_string = record_string + name + ","     
            
            for tdTag in tdTags:
                record_string = record_string + tdTag.text.strip() + ","
            
            record_string = record_string + series_num + "," +  H_A + "," + str(decade_val) +"," + str(matches_in_ser) + "\n"        
    return record_string
    
def print_in_csv(records):
    for line in records:
        if line:
            file.write(line)

def get_series_with_decades(url):
    series_wise_matches = ()
    decade_wise_series = ()
    non_bilateral = []
    partial_url = "http://www.howstat.com/cricket/Statistics/Series/"
    
    url = url.strip()
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
    return decade_wise_series, non_bilateral, series_wise_matches
        
        
        
def all_series_of_decade(url):
    odi_matches = ()
    odi_series_code = ()
    non_bilateral_series = []
    
    url = url.strip()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    odi_series = soup.find_all('tr', attrs={'bgcolor': re.compile("#")})
    count = 0

    for tr in odi_series:                                                             
        series_codes = tr.find_all('td')[0]
        link = series_codes.find('a', attrs={'class': re.compile("LinkNormal")})
        series_url = link.get('href')
        series_url = series_url.split("=")
        series_url = series_url[1]
        odi_series_code = odi_series_code + (series_url,)

        series_matches = tr.find_all('td')[2]
        link = series_matches.text.strip()
        
        odi_matches = odi_matches + (link,)
        result = tr.find_all('td')[3]
        t = result.text.strip()
        if "-" not in t and t != "":
            if t in country_names:
                non_bilateral_series.append(odi_series_code[count])
        count += 1

    return odi_series_code, non_bilateral_series, odi_matches    

if __name__ == '__main__':
    all_series_list = []
    series_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListMenu.asp#odis"
    countries_list, country_names = get_all_countries(series_url)
    decades_tuple, non_bilateral, series_wise_matches = get_series_with_decades(series_url)

    partial_url = "http://www.howstat.com/cricket/Statistics/Series/SeriesListCountry_ODI.asp?"
    for country1,country2 in list(it.combinations(countries_list,2)):
        list_series_url = partial_url + "A=" + country1 +"&B=" + country2  
        all_series_list.append(list_series_url)    
    
    df = pd.read_csv("Series_code_to_country.csv", index_col = 0)
    
    download_dir = "odi_batsman_records.csv" #where you want the file to be downloaded to 
    file = open(download_dir, "a") 
    header = "Player,Country,% Team Runs,Mat,Inns,NO,50s,100s,0s,HS,Runs,S/R,Avg,Ca,St,Series_Code, H/A, Decade_Index ,Matches\n"
    file.write(header)

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
    
