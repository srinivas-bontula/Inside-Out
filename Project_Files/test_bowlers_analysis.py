import pandas as pd
import numpy as np
from numpy import unique, inf
import matplotlib.pyplot as plt 
from functools import partial
import math

class test_bowlers:
    
    def __init__(self):
        self.country_number = {'Australia':0, 'Pakistan':1, 'New Zealand':2, 'West Indies':3, 'England':4, 'India' :5, 'Sri Lanka':6, 'Bangladesh':7, 'Zimbabwe':8, 'South Africa':9}
        self.test_bowl_df = pd.read_csv("test_bowlers_records.csv")
        self.total_entries = len(self.test_bowl_df.index)
        
    def player_appearences(self,players):
        players_dict = {}
        for i in range(self.total_entries):
            if self.test_bowl_df["Player"][i] in players_dict.keys():
                players_dict[self.test_bowl_df["Player"][i]] = players_dict[self.test_bowl_df["Player"][i]] + [i]
            else:
                players_dict[self.test_bowl_df["Player"][i]] = [i]
        return players_dict        
    
    def weighted_runs(self,series_code, series_country, series_occurances):
        trps = np.zeros(723)
        arpspc = np.zeros(10)
        tmpc = np.zeros(10)
        
        for i in range(self.total_entries):
            avg = self.test_bowl_df["Avg"][i]
            if not np.isnan(avg):
                trps[series_code[i]] += self.test_bowl_df["Runs"][i]
        
        for i in range(len(trps)):
            tmpc[series_country[i]] += self.test_bowl_df['Mat'][series_occurances[i]]
            arpspc[series_country[i]] += trps[i]      
        
        arpc = arpspc/tmpc
        weights_arpc = np.average(arpc)/arpc
        
        weighted_runs_arr = []
        for i in range(self.total_entries):
            weighted_runs_arr.append(self.test_bowl_df['Runs'][i]*weights_arpc[series_country[series_code[i]]])
        
        return weighted_runs_arr
              
    def calculate_player_metrics(self, series_code, weighted_runs_arr):
        player_metrics=np.zeros((723,4))
        balls = np.zeros(self.total_entries)
        for i in range(self.total_entries):
            avg = self.test_bowl_df["Avg"][i]
            if not np.isnan(avg):
                player_metrics[series_code[i]][0] += weighted_runs_arr[i]
                player_metrics[series_code[i]][1] += self.test_bowl_df["Wickets"][i]
                balls[i] = math.floor(self.test_bowl_df["Overs"][i])*6 + (self.test_bowl_df["Overs"][i]- math.floor(self.test_bowl_df["Overs"][i]))*10
                player_metrics[series_code[i]][2] += balls[i]
                
            player_metrics[series_code[i]][3] += self.test_bowl_df["Overs"][i]
        
        return player_metrics, balls
    
    def calculate_bowl(self,player_metrics, weighted_runs, balls, series_code):
        bowl = np.zeros((self.total_entries,3))
        for i in range(self.total_entries):
            bowl[i][0] = (player_metrics[series_code[i]][0] - weighted_runs[i])/(player_metrics[series_code[i]][1]-self.test_bowl_df["Wickets"][i])
            avg = self.test_bowl_df["Avg"][i]
            bowl[i][0] = bowl[i][0]/avg
            if np.isnan(avg) or avg == 0:
                bowl[i][0] = 0
                
        
            bowl[i][1] = (player_metrics[series_code[i]][0] - weighted_runs[i])/( player_metrics[series_code[i]][3]-self.test_bowl_df["Overs"][i])
            e_r = self.test_bowl_df["E/R"][i]
            bowl[i][1] = bowl[i][1]/e_r
            if e_r == 0:
                bowl[i][1] = 0
        
     
            bowl[i][2] = (player_metrics[series_code[i]][2]- balls[i])/(player_metrics[series_code[i]][1]-self.test_bowl_df["Wickets"][i])
            s_r = self.test_bowl_df["S/R"][i]
            bowl[i][2] = bowl[i][2]/s_r
            if np.isnan(s_r) or s_r == 0:
                bowl[i][2] = 0
        
        return bowl

        
        
    
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
                if self.test_bowl_df['H/A'][j] == 'Home' and home == 0:
                    #print(df['Country'][j])
                    series_country.append(self.country_number[self.test_bowl_df['Country'][j]]) 
                    home = home + 1
                elif self.test_bowl_df['H/A'][j] == 'Away' and away == 0:    
                    #print(df['Country'][j])
                    opposition_country.append(self.country_number[self.test_bowl_df['Country'][j]]) 
                    away = away + 1
                elif home == 1 and away == 1:
                    #print("hello")
                    break
                j = j + 1    
        return series_country, opposition_country
    

    
    
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
            elif i == (self.total_entries - 1) or self.test_bowl_df["Series_Code"][i] != self.test_bowl_df["Series_Code"][i-1]:
                if i == 19847:
                    count += 1
                x = np.array(range(count))
                x = x/count
                y = np.ones(count)-x 
                for i in y:
                    spv.append(i)
                count = 1
            elif self.test_bowl_df["Series_Code"][i] == self.test_bowl_df["Series_Code"][i-1]:
                count += 1
        
        return spv
        
    def calc_spf(self,player_names, players_app_dictionary, bowl, index, wickets):
        player_dict = {}
        for i in player_names:
            no_of_wickets=0
            spf_sum = 0
            no_series = 0
            no_balls = 0
            for j in players_app_dictionary[i]:
                spf_sum += bowl[j][index]
                no_series += 1
                no_of_wickets += self.test_bowl_df["Wickets"][j]
                #no_balls += balls[j]
            #if(no_balls > 4000):
            if(no_of_wickets > wickets):    
                player_dict[i] = spf_sum/no_series
            
        sum_values = sum(player_dict.values())
        average = sum_values/len(player_dict)
        return player_dict, average    
    
    def cumilative_spf(self, player_names, players_app_dictionary, player_metrics,weighted_runs, balls, series_code, wickets):
        bowl_arr = self.calculate_bowl(player_metrics,weighted_runs, balls, series_code)
        spf_1, avg_1 = self.calc_spf(player_names, players_app_dictionary, bowl_arr, 0, wickets)
        spf_2, avg_2 = self.calc_spf(player_names, players_app_dictionary, bowl_arr, 1, wickets)
        spf_3, avg_3 = self.calc_spf(player_names, players_app_dictionary, bowl_arr, 2, wickets)
        cumilative_avg = [avg_1, avg_2, avg_3]
        weights_avg = np.average(cumilative_avg)/cumilative_avg
        final_spv = {} 
        for i in spf_3.keys():
            final_spv[i] = (weights_avg[0]*spf_1[i]+weights_avg[1]*spf_2[i]+weights_avg[2]*spf_3[i])/np.sum(weights_avg)
    
        final_list = [(k,final_spv[k]) for k in sorted(final_spv, key=final_spv.get, reverse = True)]
        return final_list
    
    def player_lists(self, all_time, country, number=5): 
        decade_values = self.test_bowl_df['Decade_Index'].values
        total_decades, series_decade_index = unique(decade_values, return_inverse = True)  
        
        players = self.test_bowl_df['Player'].values
        player_names, player_indices = unique(players, return_index = True)
        players_app_dictionary = self.player_appearences(players)
        
        series_codes = self.test_bowl_df['Series_Code'].values
        series_list, series_occurances, series_code = unique(series_codes, return_index = True, return_inverse= True)
        
        series_country, opposition_country = self.host_and_opposition(series_occurances,series_list)
        
        weighted_runs = self.weighted_runs(series_code, series_country, series_occurances)
            
        player_metrics, balls = self.calculate_player_metrics(series_code, weighted_runs)
        
        players_list = self.cumilative_spf(player_names, players_app_dictionary, player_metrics,weighted_runs, balls, series_code, 100)
        players_list_50 = self.cumilative_spf(player_names, players_app_dictionary, player_metrics,weighted_runs, balls, series_code, 50)
        players_list_7 = self.cumilative_spf(player_names, players_app_dictionary, player_metrics,weighted_runs, balls, series_code, 7)
        #final_batsman_rankings_partial = partial(self.final_batsman_rankings, player_names,players_app_dictionary,weighted_runs, spv)
        final_player_list = []
        if all_time == "a":
            if country == "all":
                for k,v in players_list[:number]:
                    player = str(k)+':'+str(v)
                    final_player_list.append(player)
                    #print(k,"->",v)
            else:
                count=0
                for k,v in players_list:
                    first_app = player_indices[np.where(player_names == k)[0][0]]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_bowl_df['Country'][first_app] == country:
                        player = str(k)
                        final_player_list.append(player)
                        count += 1
                    if count == number:
                        break
                if count < number:
                    final_player_list = []
                    count = 0
                    for k,v in players_list_50:
                        first_app = player_indices[np.where(player_names == k)[0][0]]
                        if self.test_bowl_df['Country'][first_app] == country:
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
                    if self.test_bowl_df['Decade_Index'][first_app] >= 6:
                        count += 1
                        player = str(k)+':'+str(v)
                        final_player_list.append(player)
                    if count == number+3:
                        break
            else:
                count = 0
                for k,v in players_list:
                    first_app = player_indices[np.where(player_names == k)[0][0]]
                    #print(first,"->",df[' Decade_Index '][first])
                    if self.test_bowl_df['Country'][first_app] == country:
                        if self.test_bowl_df['Decade_Index'][first_app] >= 6:
                            count += 1
                            player = str(k)
                            final_player_list.append(player)
                            #print(k,":",v)
                        if count == 7:
                            break 
                if count < 7:
                    final_player_list = list()
                    count = 0
                    for k,v in players_list_50:
                        first_app = player_indices[np.where(player_names == k)[0][0]]
                        if self.test_bowl_df['Country'][first_app] == country:
                            if self.test_bowl_df['Decade_Index'][first_app] >= 6:
                                count += 1
                                player = str(k)
                                final_player_list.append(player)
                                #print(k,":",v)
                            if count == 7:
                                break 
        elif all_time == "next":
            count=0
            for k,v in players_list_50:
                last = players_app_dictionary[k][-1]
                #print(first)
                #print(first,"->",df[' Decade_Index '][first])
                if self.test_bowl_df['Country'][last] == country and self.test_bowl_df["Decade_Index"][last]>=13:
                    player = str(k)
                    final_player_list.append(player)
                    count += 1
                if count == 10:
                    break
            if count < 10:
                final_player_list = []
                count = 0
                for k,v in players_list_7:
                    last = players_app_dictionary[k][-1]
                #print(first)
                #print(first,"->",df[' Decade_Index '][first])
                    if self.test_bowl_df['Country'][last] == country and self.test_bowl_df['Decade_Index'][last] >= 13:
                        player = str(k)
                        final_player_list.append(player)
                        count += 1
                    if count == 10:
                        break                   
                            
        return final_player_list
                          