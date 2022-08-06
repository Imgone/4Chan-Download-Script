from concurrent.futures import thread
from abbreviations import BOARD_ABBREVIATIONS
import requests, re, json



board_selection = input("Please enter the board abbrevation you'd like to scrape\n")
abbreviation_check = True # If true, user input an abbreviation, false if using full name of board

if(board_selection in BOARD_ABBREVIATIONS.values()):
    pass
elif(board_selection in BOARD_ABBREVIATIONS):
    abbreviation_check = False
    pass
else:
    print("Board not found")
    exit()

# if user gives the name of a board, convert it to the abbreviation
if(not abbreviation_check):
    board_selection = BOARD_ABBREVIATIONS.get(board_selection)

website_url = 'https://a.4cdn.org/' + board_selection + '/threads.json'
initial_request = requests.get(website_url)
thread_num_list = []
thread_num_list_raw = json.loads(initial_request.text)

for i in range(len(thread_num_list_raw)):
    for j in range(len(thread_num_list_raw[i].get("threads"))):
        thread_num_list.append(thread_num_list_raw[i].get("threads")[j]["no"])

# this can be a check for duplicates, currently not implemented because sets are not accessible by index in python
# thread_list = set(thread_list)

thread_json_url = []

# 4chan API, gives each thread as JSON object 
# for i in range(len(thread_num_list)):
#     thread_json_url.append("https://a.4cdn.org/" + board_selection + "/thread/" + str(thread_num_list[i]) + ".json")

# print(thread_json_url)

# print(thread_num_list[0])

for i in range(len(thread_num_list)):
    total_string = ''
    total_string = ("https://a.4cdn.org/" + board_selection + "/thread/" + str(thread_num_list[i]) + ".json")
    thread_json_url.append(total_string)

# thread_json_url is now a list of every JSON api request for every thread on a board
print(len(thread_json_url))