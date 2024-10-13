#!/usr/bin/env python

from datetime import datetime
import ollama
from langchain.chains import RetrievalQA
import time, sys
import shutil
from utils.console_format import color
from utils.gen_date_range_for_google_search import generate_tbs_param
import utils.prompt_templates as prompt_templates
import extract_from_url
from google_search_api import GoogleAPIModel
import ssl
import csv, json, hashlib, os
import requests
from pathlib import Path
import urllib3


def print_available_models():
    print("Available models:")
    ollama_list = ollama.list()
    model_list = []
    for model in ollama_list['models']:
        model_list.append(model['model'])
        print(" * " + model['model'])
    print('\n')

print_available_models()

messages = []

def initialize_with_instruction(instruction, print_out_response=False):
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
  return response

def chat(messages):
    r = requests.post(
        "http://0.0.0.0:11434/api/chat",
        json={"model": MODEL, "messages": messages, "stream": True},
	stream=True
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content

        if body.get("done", False):
            message["content"] = output
            return message

def main():
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
  ssl._create_default_https_context = ssl._create_unverified_context

  USE_PERSIST_DB = False

  API = GoogleAPIModel(verbose=True)
  # Set default dataset and model to use

  MODEL = 'llama3.1:8b-instruct-fp16'

  DATASET_PATH = 'data/other-datasets/FEVER/false.txt'

  if (len(sys.argv) > 1):
      if (sys.argv[1]):
          MODEL = sys.argv[1]
      if (sys.argv[2]):
          DATASET_PATH = sys.argv[2]

  print("[INFO] You're using " + MODEL + " model now")

  time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')

  data_set_file_str = DATASET_PATH.split("/")[-1].split(".txt")[0]

  output_file_name = "logs/log_" + time_str + "_"  + data_set_file_str + ".log"
  output_csv_name = "logs/log_" + time_str + "_"  + data_set_file_str + ".csv"
  statement_hash_dataset_file_name = "data/statement_database.json"
  statement_urls_dataset_file_name = "data/url_database.json"
  csv_all_rows = []

  dict_statement_hash = {}
  dict_statement_reference = {}

  if not os.path.exists('logs'):
      os.makedirs('logs')
  if not os.path.exists('data'):
      os.makedirs('data')
  if not os.path.exists('data/snapshots'):
      os.makedirs('data/snapshots')
  '''
  ollama = Ollama(
      base_url='http://localhost:11434',
      model=MODEL,
      temperature=0,
  )
  '''
  statement_urls_dataset = Path(statement_urls_dataset_file_name)
  if statement_urls_dataset.exists():
      existing_dict_reference = json.load(open(statement_urls_dataset_file_name))
      print("[INFO] >>> Found " + str(len(existing_dict_reference.keys())) + " statement-URLs pair(s) from local storage")
  else:
      existing_dict_reference = {}

  dataset = open(DATASET_PATH, 'r')
  claims = dataset.readlines()

  print("[INFO] " + str(len(claims)) + " statements loaded...")

  with open(output_file_name,"a+", encoding='utf8') as f:
      for index, statement in enumerate(claims):
          
          statement = statement.replace("\n", "")
          print("[INFO] Inferring statement no." + str(index + 1) + " from the dataset file " + DATASET_PATH + ": " + statement)
          csv_row = [str(index + 1), "\"" + statement + "\"", DATASET_PATH.split("/")[-2]]
          f.write("[{} - Statement]\n".format(index + 1) + statement +  '\n')

          tick = time.time()
          question = prompt_templates.question_wo_langchain.format(statement=statement)
          
          message = chat([{"role": "user", "content": question}])
          
          res = message['content']
          print("[INFO] " + color.BOLD + color.CYAN + statement + color.END)
          print("[INFO] " + color.BOLD + color.GREEN + res.strip() + color.END)
          formatted_res = res.strip().replace('\n\n', '\n')

          f.write("\n[{} - Response]\n".format(index + 1) + formatted_res + '\n')
          csv_row.append(formatted_res.replace('"', '""').replace("\n", " "))

          elapsed_time = time.time() - tick    
          print("[INFO] >>> Query ended. Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
          f.write("\nElapsed time: "+ "{:.2f}".format(elapsed_time) + "s\n\n")
          csv_row.append(str(elapsed_time))
          csv_all_rows.append(csv_row)

  fields = ['No', 'Statement', 'Response', 'Response Time']
  with open(output_csv_name, 'w+', encoding='utf8') as csvfile:
      # creating a csv writer object
      csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
      # writing the dataset path for reference purposes
      csvwriter.writerow([DATASET_PATH])
      # writing the fields
      csvwriter.writerow(fields)
      # writing the data rows
      csvwriter.writerows(csv_all_rows)

if __name__=="__main__":
    main()
