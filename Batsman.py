# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv


df = pd.read_csv("records_final_series_test_final_corrected_v2.csv")

df.head(6)

series = df[' Decade_Index '].values
number, series_unique = np.unique(series, return_inverse = True)  

players = df['Player'].values
player_names, player_indices = np.unique(players, return_index = True)

player_dict_temp_3 = {}
for i in df.index:
    if df["Player"][i] in player_dict_temp_3.keys():
        player_dict_temp_3[df["Player"][i]] = player_dict_temp_3[df["Player"][i]] + [i]
    else:
        player_dict_temp_3[df["Player"][i]] = [i]
        
#print(player_dict_temp_3['Aamer Malik'])

''' finding the '''
trps = dict() #total runs per series
mps = {} # matches per series
arps = {} #average runs per series
sid = {} # series in decade
arpd = np.zeros(14)
tspd = np.zeros(14)
for i in df.index:
    x = df['Series_Code'][i]
    trps[x] = 0
    mps[x] = 0
      
for i in df.index:
    x = df['Series_Code'][i]
    trps[x] = trps[x] + df['Runs'][i]
    mps[x] = max(mps[x],df['Mat'][i])
    sid[x] = df[' Decade_Index '][i]

for i in trps.keys():
    arps[i] =trps[i]/mps[i]
    
for i in arps.keys():
    arpd[sid[i]]+= arps[i]
    tspd[sid[i]] += 1          
    
arpd = arpd/tspd
w = np.sum(arpd)/arpd
w = w/np.average(w)

'''finding the weighted runs'''
weighted_runs = np.zeros(len(df.index))
for i in df.index:
    weighted_runs[i] = df["Runs"][i]*w[df[" Decade_Index "][i]]

'''metric only with decade weights'''
runs_metric = []
player_dict_temp_4 = {}

for i in player_names:
    no_of_matches=0
    runs = 0
    for j in player_dict_temp_3[i]:
        runs += weighted_runs[j]
        no_of_matches += (df['Inns'][j] - df['NO'][j])
    if(no_of_matches > 40):    
        runs_metric.append(runs/no_of_matches)
        player_dict_temp_4[i] = (runs/no_of_matches)

Sorted_list_decade_weights = [(k,player_dict_temp_4[k]) for k in sorted(player_dict_temp_4, key=player_dict_temp_4.get, reverse = True)] 

'''printing the sorted list of all players above 40 innings'''
print('List of players using only decade weights')
fd = open('document.csv','a')
for k, v in Sorted_list_decade_weights:
    x = k + "," + str(v)+'\n'
    fd.write(x)
fd.close()
    

    
    