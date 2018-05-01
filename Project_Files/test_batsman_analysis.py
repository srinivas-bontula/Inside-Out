# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 17:26:48 2018

@author: Vasthav and Rajesh
"""

import pandas as pd
import numpy as np
from numpy import unique, inf
import matplotlib.pyplot as plt 
from functools import partial

class test_batsman:
    
    def __init__(self):
        self.country_number = {'Australia':0, 'Pakistan':1, 'New Zealand':2, 'West Indies':3, 'England':4, 'India' :5, 'Sri Lanka':6, 'Bangladesh':7, 'Zimbabwe':8, 'South Africa':9}
        self.test_df = pd.read_csv("test_batsman_statistics.csv")
        self.total_entries = len(self.test_df.index)
        
        
    def series_index_dict(self,series_list):
        dict_series={}
        for i in range(len(series_list)):
            dict_series[series_list[i]] = i
        return dict_series
    
    def player_appearences(self,players):
        players_dict = {}
        for i in range(self.total_entries):
            if self.test_df["Player"][i] in players_dict.keys():
                players_dict[self.test_df["Player"][i]] = players_dict[self.test_df["Player"][i]] + [i]
            else:
                players_dict[self.test_df["Player"][i]] = [i]
        return players_dict        
    
    def player_metrics(self):
        trps = {} # total runs per series
        mps = {} # matches per series
        arps = {} # average runs per series
        sid = {} # series in a decade
        tspd = np.zeros(14) # total series per decade
        arpd = np.zeros(14) # average runs per decade
        for i in range(self.total_entries):
            x = self.test_df['Series_Code'][i]
            trps[x] = 0
            mps[x] = 0
            #arps[x] = 0
        
        for i in range(self.total_entries):
            x = self.test_df['Series_Code'][i]
            trps[x] = trps[x] + self.test_df['Runs'][i]
            mps[x] = max(mps[x],self.test_df['Mat'][i])
            sid[x] = self.test_df[' Decade_Index '][i]
    
        for i in trps.keys():
            arps[i] =trps[i]/mps[i]
        
        for i in arps.keys():
            arpd[sid[i]]+= arps[i]
            tspd[sid[i]] += 1          
    
        arpd = arpd/tspd
        average_weights = np.sum(arpd)/arpd
        weights = average_weights/np.average(average_weights)
        return weights
    
    
    def calculate_weighted_runs(self,series_country,opposition_country,series_index_dictionary,arpsd):
        weighted_runs = np.zeros(self.total_entries)
        for i in range(self.total_entries):
        #print(i)
            index = series_index_dictionary[self.test_df['Series_Code'][i]]
            #print(series_country[index])
            #print(index)
            player_country = self.country_number[self.test_df['Country'][i]]
            weighted_runs[i] = self.test_df["Runs"][i]*arpsd[self.test_df[" Decade_Index "][i]][series_country[index]][player_country]
            
        return weighted_runs
    
    def host_and_opposition(self,series_occurances,series_list):
        opposition_country =[]
        series_country = []
        j = 0
        for i in series_occurances:
            home = 0
            away = 0
            j = i
            while 1 != 0:
                #print(j)
                if self.test_df[' H/A'][j] == 'Home' and home == 0:
                    #print(df['Country'][j])
                    series_country.append(self.country_number[self.test_df['Country'][j]]) 
                    home = home + 1
                elif self.test_df[' H/A'][j] == 'Away' and away == 0:    
                    #print(df['Country'][j])
                    opposition_country.append(self.country_number[self.test_df['Country'][j]]) 
                    away = away + 1
                elif home == 1 and away == 1:
                    #print("hello")
                    break
                j = j + 1    
        opposition_country[np.argwhere(series_list == 111)[0][0]] = 0
        opposition_country[np.argwhere(series_list == 261)[0][0]] = 3
        return series_country, opposition_country
    
    def weights_matrix_3d(self,series_occurances, series_country, opposition_country, series_index_dictionary):
        runs_per_country_decade = np.zeros((14,10,10))
        series_per_country_decade = np.zeros((14,10,10))
        series = []
        for i in range(self.total_entries):
            decade_code = self.test_df[" Decade_Index "][i]
            series_code = self.test_df['Series_Code'][i]
            index = series_index_dictionary[series_code]
            player_country = self.country_number[self.test_df["Country"][i]]
            series_country_1 = series_country[index]
            opposition_country_1 = opposition_country[index]
            Inns = self.test_df["Inns"][i]
            if  Inns== 0:
                Inns=1
            runs_per_country_decade[decade_code][series_country_1][player_country] += (self.test_df["Runs"][i]/Inns)
            if series_code not in series:
                series.append(series_code)
                series_per_country_decade[decade_code][series_country_1][series_country_1] += 1
                series_per_country_decade[decade_code][series_country_1][opposition_country_1] += 1
        return runs_per_country_decade, series_per_country_decade
    
    
    def average_runs_per_series_in_decade(self,rpcd, spcd, decade_weights):
        arpscd = rpcd/spcd
        arpscd[arpscd == inf] = 0
        np.nan_to_num(arpscd, copy=False)
        avg_arpscd= np.true_divide(arpscd.sum(1),(arpscd!=0).sum(1))
        np.nan_to_num(avg_arpscd, copy=False)
        avg_arpscd_around_1 = np.true_divide(avg_arpscd.sum(1),(avg_arpscd!=0).sum(1))
        modified_avg_arpscd = avg_arpscd_around_1[:,None,None]/arpscd
        modified_avg_arpscd[modified_avg_arpscd == inf] = 0
        total_average = decade_weights[:,None,None] * modified_avg_arpscd
        return total_average
    
    def calculate_spv(self):
        spv = []
        for i in range(self.total_entries):
            if i==0:
                count = 1
            elif i == (self.total_entries - 1) or self.test_df["Series_Code"][i] != self.test_df["Series_Code"][i-1]:
                if i == 19847:
                    count += 1
                x = np.array(range(count))
                x = x/count
                y = np.ones(count)-x 
                for i in y:
                    spv.append(i)
                count = 1
            elif self.test_df["Series_Code"][i] == self.test_df["Series_Code"][i-1]:
                count += 1
        
        return spv
        
    def final_batsman_rankings(self,player_names, players_app_dictionary, weighted_runs, spv, matches):
        player_dict = {}
        for i in player_names:
            no_of_matches=0
            runs = 0
            for j in players_app_dictionary[i]:
                runs += weighted_runs[j]*spv[j]
                no_of_matches += (self.test_df['Inns'][j] - self.test_df['NO'][j])
            if(no_of_matches > matches):    
                player_dict[i] = (runs/no_of_matches)
            
        all_batsman_list = [(k,player_dict[k]) for k in sorted(player_dict, key=player_dict.get, reverse = True)]
        return all_batsman_list    
    
    def player_lists(self, all_time, country, number=5): 
        decade_values = self.test_df[' Decade_Index '].values
        total_decades, series_decade_index = unique(decade_values, return_inverse = True)  
        
        players = self.test_df['Player'].values
        player_names, player_indices = unique(players, return_index = True)
        players_app_dictionary = self.player_appearences(players)
        
        weights = self.player_metrics()
            
        series_codes = self.test_df['Series_Code'].values
        series_list, series_occurances = unique(series_codes, return_index = True)
        
        series_index_dictionary = self.series_index_dict(series_list)
        series_country, opposition_country = self.host_and_opposition(series_occurances,series_list)
        
        rpcd, spcd = self.weights_matrix_3d(series_occurances, series_country, opposition_country,series_index_dictionary)
        arpsd = self.average_runs_per_series_in_decade(rpcd, spcd, weights)
        
        weighted_runs = self.calculate_weighted_runs(series_country, opposition_country, series_index_dictionary, arpsd)
        
        spv = self.calculate_spv()
        
        players_list = self.final_batsman_rankings(player_names,players_app_dictionary,weighted_runs, spv, 60)
        players_list_20 = self.final_batsman_rankings(player_names,players_app_dictionary,weighted_runs, spv, 20)
        
        
        #final_batsman_rankings_partial = partial(self.final_batsman_rankings, player_names,players_app_dictionary,weighted_runs, spv)
        final_player_list = []
        if all_time == "a":
            if country == "all":
                for k,v in players_list[:number]:
                    player = str(k)+':'+str(v)
                    final_player_list.append(player)
            else:
                count=0
                for k,v in players_list:
                    first_app = player_indices[np.where(player_names == k)[0][0]]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_df['Country'][first_app] == country:
                        player = str(k)
                        final_player_list.append(player)
                        count += 1
                    if count == number:
                        break
                    
                    
        elif all_time == "m":
            if country == "all":
                count = 0
                for k,v in players_list:
                    first_app = player_indices[np.where(player_names == k)[0][0]]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_df[' Decade_Index '][first_app] >= 6:
                        count += 1
                        player = str(k)+':'+str(v)
                        final_player_list.append(player)
                    if count == number:
                        break
            else:
                count = 0
                for k,v in players_list:
                    first_app = player_indices[np.where(player_names == k)[0][0]]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_df['Country'][first_app] == country:
                        if self.test_df[' Decade_Index '][first_app] >= 6:
                            count += 1
                            player = str(k)
                            final_player_list.append(player)
                        if count == number:
                            break
        
        elif all_time == "next":
            count = 0
            for k,v in players_list_20:
                    last = players_app_dictionary[k][-1]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_df['Country'][last] == country:
                        if self.test_df[' Decade_Index '][last] >= 13:
                            count += 1
                            player = str(k)
                            final_player_list.append(player)
                        if count == 10:
                            break
            
        return final_player_list


   
    
      
    


    
    
    
    
    
    
    
    
    
    
    
   
    
    

    
    
    
    
    
    
    
    
    
    
