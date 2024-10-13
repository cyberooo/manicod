#!/usr/bin/env python


import feedparser
import ollama
import time, os, hashlib, json, math
from datetime import datetime
from progress_verbose import print_progress_bar
from pathlib import Path


#MODEL = 'llama3:70b-instruct'
#MODEL = 'llama3:instruct'
MODEL = 'llama3.1:8b-instruct-fp16'

def initialize_with_instruction(instruction, print_out_response=True):
    messages = []
    messages.append(
        {
        'role': 'system',
        'content': instruction,
        }
    )
    stream = ollama.chat(model=MODEL, 
        messages=messages,
        stream=True,
    )

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        if print_out_response:
            print(part, end='', flush=True)
        response = response + part

    messages.append(
        {
        'role': 'assistant',
        'content': response,
        }
    )
    return messages

def send(prompt, messages=[], print_out_response=True):
    messages.append(
        {
        'role': 'user',
        'content': prompt,
        }
    )
    stream = ollama.chat(model=MODEL, 
        messages=messages,
        stream=True,
        options = 
        {
        'temperature': 0 # very conservative (good for coding and correct syntax)
        }
    )

    response = ""
    for chunk in stream:
        part = chunk['message']['content']
        if print_out_response:
            print(part, end='', flush=True)
        response = response + part

    messages.append(
        {
        'role': 'assistant',
        'content': response,
        }
    )
    return messages


def gen_negation(statement):
    tick = time.time()
    instruction ="<<SYS>> I will give you a statement, you need to provide me the negation of the statement. " +\
        "For example, when given \"Tom said it is a big success.\", you should output \"Tom said it is a big failure.\"" +\
        "Another example, when given \"The weather today is good.\", you should output \"The weather today is bad.\"" +\
        "Remember, try to make minimal modication over the original statement. Try to use antonym rather than merely inserting a \"not\". " +\
        "Only output the negatiion version of the statement. Output \"Not applicable\" if there does not exist a negation. <</SYS>>"
    
    messages = initialize_with_instruction(instruction, print_out_response=False)
    messages = send(statement, messages, print_out_response=False)
    result = messages[-1]['content'].strip().replace('\n\n', '\n')
    elapsed_time = time.time() - tick
    return result  


def alter_context(statement):
    tick = time.time()
    instruction ="<<SYS>> I will give you a statement, you need to extract if there is any context about quantity, number, percentage, year, " +\
        "time, date, person name who are famous (e.g., Obama, Taylor Swift, etc), country, city, or any other geographical concept from it. " +\
        "You also need to use parentheses \"()\" to enclose the extracted text. " +\
        "For example, when given \"Tom said he went to Los Angeles on last Saturday.\", you should output \"(Tom) said he went to (Los Angeles) on last (Saturday).\"" +\
        "For example, when given \"Families face £1,045 bill for summer holiday clubs: The cost of holiday provision has risen by 6\% across Great Britain\", " +\
        "you should output \"Families face £(1,045) bill for summer holiday clubs: The cost of holiday provision has risen by (6\%) across (Great Britain)\". " +\
        "Another example, when given \"Barack Obama is the 44th president of the United States from 2009 to 2017.\", " +\
        "you should output \"(Barack Obama) is the (44th) president of (the United States) from (2009) to (2017).\"" +\
        "Remember, try to make minimal modication over the original statement. You should post a conservative stance, do not change if you are not sure. " +\
        "Do not mark a title (e.g., director, secretary), appointment name (e.g., Prime Minister), or an entity name (e.g., government, university, etc). " +\
        "Only output the statement with your parentheses. Output \"Not applicable\" if you cannot find anything. <</SYS>>"
    
    messages = initialize_with_instruction(instruction, print_out_response=False)
    messages = send(statement, messages, print_out_response=False)
    result = messages[-1]['content'].strip().replace('\n\n', '\n')
    elapsed_time = time.time() - tick
    #verbose_difference(statement, result)
    return result  


def verbose_difference(str1, str2):
   print(str1)
   length = len(str1)
   left_half = math.floor((length - 4) / 2)
   print('-' * left_half + ' VS ' + '-' * (length - left_half))
   print(str2)
   

def dump_json(dict, json_file_path):
    news_synthesis_dataset = Path(json_file_path)
    if news_synthesis_dataset.exists():
       all_news = json.load(open(json_file_path))
       # print(">>> Found " + str(len(all_news.keys())) + " news from local storage")
       all_news.update(dict)
       json.dump(all_news, open(json_file_path, 'w+'), ensure_ascii=False, indent=4)
    else:
       json.dump(dict, open(json_file_path, 'w+'), ensure_ascii=False, indent=4)
    
def synthesis_news():
    feed_files = []
    path = "data/data_collection/"
    dir_list = os.listdir(path)
    for f in dir_list:
        if f.endswith(".log"):
            feed_files.append(f)
    print(str(len(feed_files)) + " files found in ", path)

    news_dict = {}
    date_str = datetime.now().strftime('%Y%m%d')
    news_synthesis_dataset_file_name = "data/news_synthesis_" + date_str + ".json"
    
    print_progress_bar(0, len(feed_files), prefix = 'Progress:', suffix = 'Complete', length = 50)
            
    for f_index, fn in enumerate(feed_files):
        prefix_str = '[' + str(f_index + 1) + '/' + str(len(feed_files)) + ']:'
        with open(os.path.join(path, fn)) as file:
            lines = file.readlines()
            for line_index, line in enumerate(lines):
                print_progress_bar(line_index, len(lines), prefix = prefix_str, suffix = 'Processing filename ' + fn, length = 50)
                if line.endswith('?'):
                   continue

                curr_news = {}

                line = line.strip()
                if not line.endswith('!') and not line.endswith('.'):
                    line = line + '.'
                news_hash = hashlib.md5(line.encode()).hexdigest()
                
                news_dict[news_hash] = {}
                news_dict[news_hash]['original'] = line
                print_progress_bar(line_index + 0.3, len(lines), prefix = prefix_str, suffix = 'Processing filename ' + fn, length = 50)
                news_dict[news_hash]['neg'] = gen_negation(line)
                print_progress_bar(line_index + 0.7, len(lines), prefix = prefix_str, suffix = 'Processing filename ' + fn, length = 50)
                news_dict[news_hash]['context'] = alter_context(line)

                source = fn[:fn.find("_202")]
                news_dict[news_hash]['source'] = source
                date = fn[fn.find("_202") + 1:-4]
                date = date[:date.rfind("-")]
                news_dict[news_hash]['date'] = date
                
            print_progress_bar(len(lines), len(lines), prefix = prefix_str, suffix = 'Complete filename ' + fn +' ' * 5, length = 50)
        dump_json(news_dict, news_synthesis_dataset_file_name) 
    

if __name__ == "__main__":
    synthesis_news()