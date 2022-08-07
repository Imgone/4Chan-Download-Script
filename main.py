from concurrent.futures import ThreadPoolExecutor, thread
from threading import Thread,local
from requests.sessions import Session
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


for i in range(len(thread_num_list)):
    total_string = ''
    total_string = ("https://a.4cdn.org/" + board_selection + "/thread/" + str(thread_num_list[i]) + ".json")
    thread_json_url.append(total_string)

# thread_json_url is now a list of every JSON api request for every thread on a board

thread_json_data = []
#now we need to parse the new json_url with a loop

thread_local = local()

def get_session() -> Session:
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session

def download_link(url:str):
    session = get_session()

    with session.get(url) as response:
        thread_json_data.append(response.json())
# print(thread_json_url)
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(download_link, thread_json_url)

image_link_list = []
# print(thread_json_data[0]["posts"][0]["tim"])
def check_for_image(i, j):
    try:
        thread_json_data[i]["posts"][j]["tim"]
        return True
    except:
        return False

for i in range(len(thread_json_data)):
    for j in range(len(thread_json_data[i]["posts"])):
        # print(j)
        if(check_for_image(i,j)):
            img_id = str(thread_json_data[i]["posts"][j]["tim"])
            img_ext = thread_json_data[i]["posts"][j]["ext"]
            # print("https://i.4cdn.org/"+board_selection+"/"+img_id+img_ext)
            image_link_list.append("https://i.4cdn.org/"+board_selection+"/"+img_id+img_ext)
        else:
            continue
        

# download all images

# for i in range(len(image_link_list)):

#     img_data = requests.get(image_link_list[i]).content
#     with open('')
print(image_link_list)