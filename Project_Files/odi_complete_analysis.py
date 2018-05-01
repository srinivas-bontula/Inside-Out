import odi_batsman_analysis as obat
import odi_bowlers_analysis as obowl
from time import sleep
import warnings

if __name__ == '__main__':
    batsman = obat.odi_batsman()
    bowlers = obowl.odi_bowlers()
    warnings.filterwarnings('ignore')  
    number = 5
    countries = {0: "all", 1: "Australia", 2:"Bangladesh" , 3:"England", 4:"India", 5:"New Zealand", 6:"Pakistan", 7:"South Africa", 8: "Sri Lanka", 9:"West Indies", 10: "Zimbabwe"}
    print("Welcome to ODI analysis")
    op_input = input('Batting -> Bat \nBowling -> Bowl \nTeam -> Team \n Select which analysis: ')
    if op_input.lower() == 'team':
        option_input = input('all_time -> a\nmodern -> m\nsquad_prediction -> next\nselect one of the options: ')
        country_no = int(input('Australia -> 1 \nBangladesh -> 2 \nEngland -> 3 \nIndia -> 4 \nNew Zealand -> 5 \nPakistan -> 6 \nSouth Africa -> 7 \nSri Lanka -> 8 \nWest Indies -> 9 \nZimbabwe-> 10 \nEnter the country from above list: '))
        country = countries[country_no]
        players_bat = batsman.player_lists(option_input, country, number)
        players_bowl = bowlers.player_lists(option_input, country, number)
        count = 0
        if option_input == "next":
            print("\n")
            for k in players_bat:
                print(k)
                count += 1
            for i in players_bowl:
                if i not in players_bat:
                    print(i)
                    count += 1
                if count == 20:
                    break
        else:
            print("\n")
            for k in players_bat:
                print(k)
                count += 1
            for i in players_bowl:
                if i not in players_bat:
                    print(i)
                    count += 1
                if count == 20:
                    break
    elif op_input.lower() == 'bat':
        option_input = input('all_time -> a\nmodern -> m\nselect one of the options: ')
        country_no = int(input('All -> 0 \nAustralia -> 1 \nBangladesh -> 2 \nEngland -> 3 \nIndia -> 4 \nNew Zealand -> 5 \nPakistan -> 6 \nSouth Africa -> 7 \nSri Lanka -> 8 \nWest Indies -> 9 \nZimbabwe-> 10 \nEnter the country from above list: '))
        country = countries[country_no]
        if country_no== 0:
            number = int(input("Number of Players: "))
        players_bat = batsman.player_lists(option_input, country, number)
        print("\n")
        for k in players_bat:
            print(k)
    
    elif op_input.lower() == 'bowl':
        option_input = input('all_time -> a\nmodern -> m\nselect one of the options: ')
        country_no = int(input('All -> 0 \nAustralia -> 1 \nBangladesh -> 2 \nEngland -> 3 \nIndia -> 4 \nNew Zealand -> 5 \nPakistan -> 6 \nSouth Africa -> 7 \nSri Lanka -> 8 \nWest Indies -> 9 \nZimbabwe-> 10 \nEnter the country from above list: '))
        country = countries[country_no]
        if country_no == 0:
            number = int(input("Number of Players: "))
        players_bowl = bowler.player_lists(option_input, country, number)
        print("\n")
        for k in players_bowl:
            print(k)
    sleep(60)
    
        
        