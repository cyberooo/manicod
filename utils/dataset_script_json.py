#!/usr/bin/env python


import json, re, math, time, os, sys
from pathlib import Path
from collections import OrderedDict, defaultdict

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
news_source_full_name = {
    'google_news_us': 'Google News US',
    'google_news_uk': 'Google News UK',
    'google_news_ca': 'Google News Canada',
    'google_news_au': 'Google News Australia', 
    'google_news_nz': 'Google News New Zealand', 
    'google_news_za': 'Google News South Africa', 
    'google_news_sg': 'Google News Singapore', 
    'fox_world': 'Fox World News',
    'fox_politics': 'Fox Politics News',
    'fox_sports': 'Fox Sports News',
    'fox_health': 'Fox Health News',
    'fox_science': 'Fox Science News',
    'nyt_world': 'New York Times World News',
    'nyt_business': 'New York Times Business News',
    'nyt_tech': 'New York Times Technology News',
    'nyt_sports': 'New York Times Sports News',
    'nyt_science': 'New York Times Science News',
    'nyt_health': 'New York Times Health News',
    'bbc_world': 'New York Times World News',
    'bbc_business': 'BBC Business News',
    'bbc_politics': 'BBC Politics News',
    'bbc_ent_n_arts': 'BBC Entertainment and Arts News',
    'bbc_health': 'BBC Health News',
    'bbc_sci_n_environ': 'BBC Science and Environment News',
    'bbc_education': 'BBC Education News',
    'bbc_tech': 'BBC Technology News',
    'cna_asia': 'CNA Asia News',
    'cna_sgp': 'CNA Singapore News',
}


def plot_summary(data):
    data = dict(sorted(data.items()))
    max_len_key = 0
    max_num_value = 0
    for key in data.keys():
        value = data[key]
        if len(key) > max_len_key:
            max_len_key = len(key)
        if value > max_num_value:
            max_num_value = value
    
    #print("=" * 85)
    #title_str = " Summary of Processed News by Source "
    #print(" " * math.ceil((85 - len(title_str))/2) + title_str + " " * math.floor((85 - len(title_str))/2))
    print("-" * 85)
    for key in data.keys():
        value = data[key]
        print(key, " " * (max_len_key - len(key)), end = "")
        print("| " + "*" * int(50 * value / max_num_value) + " " * (60 - int(50 * value / max_num_value)), end="")
        print('{:>5}'.format('('+str(value)+')'))
    #print("=" * 85)

def count_value_occurrences(json_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    
    # Initialize a dictionary to hold the frequency counts
    value_counts = defaultdict(lambda: defaultdict(int))

    # Iterate through the data
    for entry in data:
        for key, value in data[entry].items():
            if key != 'text' and key!= 'digest' and key!= 'note':
                value_counts[key][value] += 1

    return value_counts


def summary(db_index_path, db_misinfo_neg_path, db_misinfo_ctx_path):
    num_news_index = 0
    num_misinfo_neg = 0
    num_misinfo_ctx = 0
    
    if Path(db_index_path).exists():
        with open(db_index_path) as f:
            dict_from_file = json.load(f)
            num_news_index = len(dict_from_file.keys())
    
    if Path(db_misinfo_neg_path).exists():
        with open(db_misinfo_neg_path) as f:
            dict_from_file = json.load(f)
            num_misinfo_neg = len(dict_from_file.keys())
    
    if Path(db_misinfo_ctx_path).exists():
        with open(db_misinfo_ctx_path) as f:
            dict_from_file = json.load(f)
            num_misinfo_ctx = len(dict_from_file.keys())

    print("*" * 33 + " Database Summary " + "*" * 34)
    print("Number of news (negation/context/total): " +  str(num_misinfo_neg) + "/" +\
          str(num_misinfo_ctx) + "/" + str(num_news_index))
    #print("Number of News record: " + str(num_news_index))
    #print("Number of Fake News (Negation) record: " + str(num_misinfo_neg))
    #print("Number of Fake News (Context) record: " + str(num_misinfo_ctx))
    #print("*" * 85)

def search_json_key_exists(key, json_file_path):
    dataset = Path(json_file_path)
    if dataset.exists():
        with open(json_file_path, encoding='utf8') as f:
            dict_from_file = json.load(f)
            if key in dict_from_file.keys():
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


def highlight_text_with_parenthesis(text, show_assist_line=True):
    left_parenthesis_indexes = [m.start(0) for m in re.finditer(r'\(.*?\)', text)]
    right_parenthesis_indexes = [m.end(0) for m in re.finditer(r'\(.*?\)', text)]
    

    if len(left_parenthesis_indexes) > 0:
        text_to_display = ""
        left_idx = 0
        right_idx = 0
    
        assist_line = ""
        assist_label_count = 0

        for idx, l_p_index in enumerate(left_parenthesis_indexes):
            right_idx = left_parenthesis_indexes[idx]
            text_to_display += text[left_idx:right_idx]

            assist_line += " " * (right_idx - left_idx)

            text_to_display += color.BOLD + color.BLUE + text[l_p_index:right_parenthesis_indexes[idx]] + color.END

            assist_label_length = right_parenthesis_indexes[idx] - l_p_index
            assist_line += "-" * math.ceil((assist_label_length - 1)/2)
            assist_line += str(assist_label_count)
            assist_line += "-" * math.floor((assist_label_length - 1)/2)
            assist_label_count += 1

            left_idx = right_parenthesis_indexes[idx]
        
        text_to_display += text[left_idx:]

        if show_assist_line:
            text_to_display += "\n" + assist_line

        return text_to_display
    else:
        return text
        

def modify_context_according_to_user_input(text, context_indices):
    left_parenthesis_indexes = [m.start(0) for m in re.finditer(r'\(.*?\)', text)]
    right_parenthesis_indexes = [m.end(0) for m in re.finditer(r'\(.*?\)', text)]

    modification_record = []
    new_text = ""
    left_idx = 0
    right_idx = 0

    for context_index in context_indices:
        if context_index < len(left_parenthesis_indexes):
            right_idx = left_parenthesis_indexes[context_index]
            new_text += text[left_idx:right_idx]
            
            context_word = text[left_parenthesis_indexes[context_index]:right_parenthesis_indexes[context_index]]
            
            replacement_word = input(" >>>>>>>> " + context_word + " -> ")
            new_text += replacement_word
            modification_record.append(context_word + " -> (" + replacement_word + ")")

            left_idx = right_parenthesis_indexes[context_index]
        else:
            print("[WARNING] The index from the input is out of the range, skipped.")
    new_text += text[left_idx:]
    return new_text, modification_record

      
def upsert_negation_fake_news(db_misinfo_neg_path, digest, text, source):
    fake_news_dict = {}
    fake_news_item = {}
    fake_news_item["digest"] = digest
    fake_news_item["text"] = text
    fake_news_item["type"] = "NEGATION"
    if source in news_source_full_name.keys():
        fake_news_item["source"] = news_source_full_name[source]
    else:
        fake_news_item["source"] = source
    fake_news_dict[digest] = fake_news_item
    #db_misinfo_neg.upsert(fake_news_item, Query().digest == digest)
    dump_json(fake_news_dict, db_misinfo_neg_path) 
    print("[INFO] The negation of the selected news has been added into the databse")
            
def upsert_context_fake_news(db_misinfo_ctx_path, digest, text, source):
    fake_news_item = {}
    fake_news_item["digest"] = digest
    fake_news_item["type"] = "CONTEXT"
    if source in news_source_full_name.keys():
        fake_news_item["source"] = news_source_full_name[source]
    else:
        fake_news_item["source"] = source
    print("[INFO] Select which context would you like to modify...")
    print(highlight_text_with_parenthesis(text))

    user_input_indices = input(" >>>>>> Enter the indices of the highlighted context words that you want to modify, separated by space (Type in [Q] to skip): ")

    input_int_list = []
    if 'q' in user_input_indices or 'Q' in user_input_indices:
        return None
    
    for idx in user_input_indices.split(" "):
        try:
            input_int_list.append(int(idx))
        except:
            print("[WARNING] Partial of your input [" + idx + "] cannot be converted to integer, skipped.")
    input_int_list.sort() # Sort the list
    input_int_list = list(set(input_int_list)) # Remove duplicate
    modified_news, list_of_changes = modify_context_according_to_user_input(text, input_int_list)
    
    modified_news_clean = modified_news.replace("(", "").replace(")", "")
    fake_news_item["text"] = modified_news_clean
    fake_news_item["note"] = ", ".join(list_of_changes)
    
    #db_misinfo_ctx.upsert(fake_news_item, Query().digest == digest)
    fake_news_dict = {}
    fake_news_dict[digest] = fake_news_item
    dump_json(fake_news_dict, db_misinfo_ctx_path) 
    print("[INFO] The modification has been added into the databse: " + modified_news_clean)
    
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')
               
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Please only call me with one parameter")
        sys.exit()
    elif len(sys.argv) == 2:
        date_str = sys.argv[1]
    else:
        date_str = '20240724'


    # Set the path of the file BELOW:
    #JSON_PATH = 'data/data_collection/processed/news_synthesis_20240726.json'
    JSON_PATH = 'data/news_synthesis.json'
    f = open(JSON_PATH)

    #date_str = JSON_PATH[:-5].split('_')[-1]
    db_misinfo_neg_path = "data/fake_news_negation_" + date_str + ".json"
    db_misinfo_ctx_path = "data/fake_news_context_" + date_str + ".json"
    db_index_path = "data/news_index_" + date_str + ".json" # Collection of all news covered in our dataset


    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    if date_str not in data:
        print("The date string provided (" + date_str + ") cannot be found in the news dataset. Terminating...")
        exit()
    else:
        print("Welcome! You have typed in " + date_str + " for the news sorting task. ")
    date_selected_date = OrderedDict(sorted(data[date_str].items()))
    #date_selected_date = OrderedDict(sorted(date_selected_date.items()))
    
    print("There are " + str(len(date_selected_date.keys())) + " news entities found for this date.")
    
    for key, value in date_selected_date.items():
        
        valid_user_input = False

        orig_text = value["original"]
        source = value["source"]
        date = value["date"]

        #query = Query()
        #if db_index.search(query.digest == key):
        if search_json_key_exists(key, db_index_path):
            print("[INFO] News " + key + " has been added into the databse, skipped.")
            continue

        if Path(db_index_path).exists():
            summary(db_index_path, db_misinfo_neg_path, db_misinfo_ctx_path)
            #news_distribution = count_value_occurrences(db_index_path)
            #plot_summary(news_distribution['source'])

        print("="*85)
        print(color.BOLD + color.BLUE + "Digest" + color.END + ": " + key)
        print(color.BOLD + color.BLUE + "Source" + color.END + ": " + source, end='\t')
        print(color.BOLD + color.BLUE + "Date" + color.END + ": " + date)
        print(color.BOLD + color.BLUE + "Text" + color.END + ": " + orig_text)
        print(color.BOLD + color.BLUE + "Negation" + color.END + ": " + value["neg"])
        print(color.BOLD + color.BLUE + "Context" + color.END + ": " + value["context"])
        print("="*85)

        news_item = {}
        news_dict = {}
        news_item["digest"] = key
        news_item["text"] = value["original"]
        news_item["source"] = value["source"]
        news_item["date"] = value["date"]

        user_choice = input(" >>> Enter your choice (include [N] for negation. [C] for context modification. [Q] to quit. OTHERWISE, this news will be skipped): ")

        if 'n' in user_choice or 'N' in user_choice:
            valid_user_input = True
            
            #db_index.upsert(news_item, query.digest == key)
            news_dict[key] = news_item
            dump_json(news_dict, db_index_path) 
            upsert_negation_fake_news(db_misinfo_neg_path, key, value["neg"], source)   

        if 'c' in user_choice or 'C' in user_choice:
            valid_user_input = True

            #db_index.upsert(news_item, query.digest == key)
            news_dict[key] = news_item
            dump_json(news_dict, db_index_path) 
            upsert_context_fake_news(db_misinfo_ctx_path, key, value["context"], source)

        if 'q' in user_choice or 'Q' in user_choice:
            valid_user_input = True
            break

        if not valid_user_input:
            print("\n[INFO] Your input [" + user_choice + "] is not recognized. ", end="")    
            print("The current news is skipped...")
            screen_clear()
            continue
        print('\n')
        time.sleep(1)
        screen_clear()
        
    # Closing file
    f.close()
    
    if Path(db_index_path).exists():
        screen_clear()
        summary(db_index_path, db_misinfo_neg_path, db_misinfo_ctx_path)
        news_distribution = count_value_occurrences(db_index_path)
        plot_summary(news_distribution['source'])

