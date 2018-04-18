# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 00:19:09 2018

@author: Vasthav
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 01:58:58 2018

@author: Vasthav
"""
import requests
import re
from bs4 import BeautifulSoup
#import time
import random
import itertools as it
import threading

final_list = []
#records = []
"""
proxies_list = ['64.183.94.45:8080', '62.74.237.178:3128','202.69.38.82:8080',
'37.59.115.136:3128',
'103.26.246.22:8080',
'85.11.114.135:3128',
'124.124.1.178:3128',
'137.74.168.174:8080',
'176.31.174.1:9999',
'13.229.121.73:3128',
'144.76.176.72:8080',
'128.199.167.199:8080',
'93.189.83.85:8081',
'89.28.53.42:8080',
'140.86.97.76:80',
'138.0.152.163:3128',
'176.9.28.86:3128',
'125.212.207.121:3128',
'179.185.16.21:3130',
'187.1.51.122:80',
'64.173.224.142:9991',
'137.74.168.174:80',
'195.80.140.212:8081',
'101.50.1.2:80',
'67.78.143.182:8080',
'101.50.1.2:80',
'67.78.143.182:8080',
'104.131.177.129:8080',
'45.77.150.51:8888',
'82.149.207.86:8081',
'217.182.76.229:8888',
'37.187.125.144:3128',
'212.237.37.152:3128',
'192.99.55.120:3128',
'145.239.92.106:3128',
'129.18.144.54:8080',
'93.184.160.246:8080',
'210.4.65.230:8080',
'128.199.167.199:80',
'139.59.109.146:3128',
'122.155.222.98:3128',
'61.7.167.53:3128',
'187.58.65.225:3128',
'41.160.222.44:8080',
'5.249.147.146:3128',
'181.48.234.35:3128',
'85.132.138.22:3128',
'190.121.158.122:8080',
'190.24.131.250:3128',
'212.237.23.60:2000',
'125.212.207.121:3128',
'139.59.109.146:3128',
'139.59.109.146:8080',
'179.185.16.21:3130',
'139.59.2.223:8888',
'217.61.15.26:3128',
'67.78.143.182:8080',
'13.73.16.134:8080',
'192.99.55.120:3128',
'31.182.52.156:3129',
'185.76.147.151:3128',
'145.239.92.106:3128',
'147.135.210.114:54566',
'151.80.140.233:54566',
'37.187.125.144:3128',
'163.172.211.176:3128',
'163.172.220.221:8888',
'190.7.112.18:3130',
'158.69.48.38:3128',
'79.137.42.124:3128',
'217.61.15.26:80',
'51.15.137.26:3128',
'85.11.114.135:3128',
'181.196.50.238:65103',
'144.76.176.72:8080',
'187.108.38.214:65309',
'31.25.141.148:8080',
'137.74.168.174:8080',
'91.192.2.168:53281',
'210.57.214.46:3128',
'203.189.89.153:8080',
'190.151.10.226:8080',
'83.241.46.175:8080',
'109.236.113.1:8080',
'201.221.128.27:8080',
'202.56.203.40:80',
'137.74.168.174:80',
'195.209.107.148:3128',
'139.59.125.12:80',
'92.185.220.118:8080',
'129.18.144.54:8080',
'213.174.123.194:3128',
'13.92.101.180:80',
'13.229.121.73:3128',
'201.184.139.243:3128',
'122.248.100.5:8080',
'51.140.186.89:80',
'111.67.71.12:8080',
'43.255.22.186:8080',
'181.189.235.11:8080',
'182.253.106.14:8080',
'31.179.240.169:53281',
'84.22.35.37:3129',
'103.15.251.75:80',
'37.187.119.226:3128',
'187.115.67.227:3128',
'203.189.149.81:65103',
'107.161.9.162:8080',
'187.110.238.133:3130',
'1.179.203.10:8080',
'186.47.83.126:80',
'1.179.156.233:8080',
'180.183.245.217:8080',
'180.234.223.202:8080',
'187.72.166.10:8080',
'103.10.169.99:3128',
'186.47.83.126:8080',
'178.33.76.75:8080',
'212.83.164.85:80',
'200.29.191.151:3128',
'64.173.224.142:9991',
'103.1.238.91:3128',
'121.129.127.209:80',
'109.248.236.92:8080',
'180.211.91.130:8080',
'190.15.222.53:8080',
'182.253.236.74:8080',
'104.236.175.143:80',
'216.198.170.70:8080'
 ]  """

proxies_list = ['195.80.140.212:8081', '187.110.238.133:3130']

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
        appended_url = series_url + '&Scope=All#bat'
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
    batting_records = soup.find('div', attrs={'id': re.compile("bat")})
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
            #print(tdTag.text)
            #record.append(tdTag.text.strip())
            record_string = record_string + tdTag.text.strip() + ","
        
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
    for line in records:
        file.write(line)
    #file.close()

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
    proxies['http'] = random.choice(proxies_list)
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
    download_dir = "records_final_series_test_final_corrected_v1.csv" #where you want the file to be downloaded to 
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
    #print_in_csv(series_list)
    
