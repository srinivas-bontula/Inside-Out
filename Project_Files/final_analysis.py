import os 

format_input = input("Select Test or ODI: ")
if format_input.lower() == "odi":
    os.system('python odi_complete_analysis.py')
elif format_input.lower() == "test":
    os.system('python test_complete_analysis.py')
    