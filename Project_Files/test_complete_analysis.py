# -*- coding: utf-8 -*-
"""
Created on Tue May  1 14:34:43 2018

@author: Vasthav
"""
import test_batsman_analysis as tbat
import test_bowler_analysis as tbowl
import warnings
import sys

if __name__ == '__main__':
    batsman = tbat.test_batsman()
    bowler = tbowl.test_bowler()
    warnings.filterwarnings('ignore')  
    print("Welcome to test analysis")
    option_input = input('all_time -> a\nmodern -> m\nsquad_prediction -> next\nselect one of the options: ')
    if option_input == "next":
        country = input('Australia\nBangladesh\nEngland\nIndia\nNew Zealand\nPakistan\nSouth Africa\nSri Lanka\nWest Indies\nZimbabwe\nEnter the country from above list: ')
    else:
        country = input('All \nAustralia \nBangladesh \nEngland \nIndia \nNew Zealand \nPakistan \nSouth Africa \nSri Lanka \n West Indies \nZimbabwe \nEnter the country from above list: ')
        if country.lower() == "all":
            number = input("Number of Players: ")
    players_bat = batsman.player_lists(option_input, country, number)
    players_bowl = bowler.player_lists(option_input, country, number)
    print(players_bat)   