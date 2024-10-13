#!/usr/bin/env python

from datetime import datetime
import csv, json, hashlib, os
from pathlib import Path
from collections import OrderedDict, defaultdict

def search_json_key_exists_in_any_date(key, json_file_path):
    dataset = Path(json_file_path)
    if dataset.exists():
        with open(json_file_path) as f:
            dicts_from_file = json.load(f)
            for date_key, value_by_date in dicts_from_file.items():
                # print(" > checking the key " + key + " in " + date_key + "...")
                if key in value_by_date.keys():
                    return True
    return False

def dump_json(dict, json_file_path):
    news_synthesis_dataset = Path(json_file_path)
    if news_synthesis_dataset.exists():
       all_news = json.load(open(json_file_path))
       all_news.update(dict)
       json.dump(all_news, open(json_file_path, 'w+'), ensure_ascii=False, indent=4)
    else:
       json.dump(dict, open(json_file_path, 'w+'), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    all_in_one_json_path = "data/news_synthesis.json" # Collection of all news covered in our dataset

    dict_synthesis_news_per_day = 'data/data_collection/processed'
    list_synthesis_news_per_day = []
    directory = os.fsencode(dict_synthesis_news_per_day)
    count = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and filename.startswith("news_synthesis_20240"):
            count += 1
            list_synthesis_news_per_day.append(dict_synthesis_news_per_day + "/" + filename)
    
    list_synthesis_news_per_day.sort()
    print("Synthesis news for " + str(count) + " days identified in directory " + dict_synthesis_news_per_day)
    
    for JSON_PATH in list_synthesis_news_per_day:
        # Set the path of the file BELOW:
        #JSON_PATH = 'data/data_collection/processed/news_synthesis_20240725.json'
        f = open(JSON_PATH)

        date_str = JSON_PATH[:-5].split('_')[-1]

        json_data = {}
        json_dict_by_current_date = {}

        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        data = OrderedDict(sorted(data.items()))
        # Iterating through the json
        # list
        for key, value in data.items():
            
            #query = Query()
            if search_json_key_exists_in_any_date(key, all_in_one_json_path):
                #print("[INFO] News " + key + " has been added into the databse, skipped.")
                continue
            json_dict_by_current_date[key] = value
            print(".", end="")
        
        print()
        json_data[date_str] = json_dict_by_current_date
        print(str(len(json_dict_by_current_date.keys())) + " entities " + date_str + " has been added into the all-in-one json file.")
        
        dump_json(json_data, all_in_one_json_path)

    print("Finished.")