The following are the instructions for executing the python files to collect data and to get results of analysis:

Data Collection:
1. Tests:
	Execute the python files(test_batsman_data.py and test_bowlers_data.py). 
	The result would be 2 CSV files(test_batsman_records.csv and test_bowlers_records.csv respectively)
	The overall execution should take 3 minutes for each file.

2. ODIS:
	Execute the python files(odi_batsman_data.py and odi_bowlers_data.py). 
	The result would be 2 CSV files(odi_batsman_records.csv and odi_bowlers_records.csv respectively)
	The overall execution should take 3 minutes for each file.

Results:

Enter the following code in Command Prompt (with the folder address):
	
python final_analysis.py

Then it prompts to select Test or ODI's: 
	Enter "test" for Test analysis
	Enter "odi" for One-Day Internationals analysis

Then it prompts to select the type of analysis:
	Enter "bat" for batting analysis
	Enter "bowl" for bowling analysis
	Enter "team" for team analysis

For Team Analysis:
	Then it prompts to select Time Period:
		Enter "a" for all-time
		Enter "m" for modern(after 80's for tests and after 95's for ODIs)
		Enter "next" for squad prediction

	Then it prompts to select the country:
		Enter the country number for a specific country
		for all time(it displays the all time team XI's)
		for modern(it displays the modern team XI's)(i.e Debut after 1980 for Tests and Debut after 1995 for ODIs)
		for next(it displays the predicted team for "Next Series for Tests" and "World-Cup for ODIs)

For Batting or Bowling Analysis:
	
	Then it prompts to select the country:
		Enter the country number for a specific country: (it displays the top 5 players for the country)
		Enter 0 for all teams: (This prompts for number of players to display)
	
	for all teams:
		Enter the number of top players to be displayed: (this displays the top players for the batting or bowlers for all teams)






	