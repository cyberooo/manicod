#!/usr/bin/env python

from datetime import datetime
from langchain_community.llms import Ollama

from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

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
from pathlib import Path
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

USE_PERSIST_DB = False

API = GoogleAPIModel(verbose=True)
# Set default dataset and model to use

MODEL = 'llama3.1:8b-instruct-fp16'

DATASET_PATH = 'data/other-datasets/LIAR-RAW/true.txt'

if (len(sys.argv) > 1):
    if (sys.argv[1]):
        MODEL = sys.argv[1]
    if (sys.argv[2]):
        DATASET_PATH = sys.argv[2]

print("[INFO] You're using " + MODEL + " model now")

time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')

CHROMA_PERSIST_DIR = "./chroma_db_" + time_str

data_set_file_str = DATASET_PATH.split("/")[-1].split(".txt")[0]

#output_file_name = "logs/log_" + time_str + "_"  + MODEL.replace(':','-') + ".log"
#output_csv_name = "logs/log_" + time_str + "_"  + MODEL.replace(':','-') + ".csv"
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

ollama = Ollama(
    base_url='http://localhost:11434',
    model=MODEL,
    temperature=0,
)

oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")

statement_urls_dataset = Path(statement_urls_dataset_file_name)
if statement_urls_dataset.exists():
    existing_dict_reference = json.load(open(statement_urls_dataset_file_name))
    print("[INFO] >>> Found " + str(len(existing_dict_reference.keys())) + " statement-URLs pair(s) from local storage")
else:
    existing_dict_reference = {}

dataset = open(DATASET_PATH, 'r')
claims_n_reports = dataset.readlines()

statements = []
reports = []

domains = []
google_gl_countries = []
news_source = []

temp_reports_list_for_curr_claim = []
for line in claims_n_reports:
    if not line.startswith('*****') and len(line.strip()) > 0:
        # Save all cached reports for the last claim
        if len(temp_reports_list_for_curr_claim) > 0:
            reports.append(temp_reports_list_for_curr_claim)
            temp_reports_list_for_curr_claim = []
        statements.append(line.strip().replace("\n", " "))
    else: # Reports for current claim are starting with "*****"
        temp_reports_list_for_curr_claim.append(line[5:].strip().replace("\n", " "))
# Save the last claim's reports
if len(temp_reports_list_for_curr_claim) > 0:
    reports.append(temp_reports_list_for_curr_claim)

print("[INFO] " + str(len(statements)) + " statements loaded...")

with open(output_file_name,"a+", encoding='utf8') as f:
    for index, statement in enumerate(statements):
        
        statement = statement.replace("\n", "")
        print("[INFO] Inferring statement no." + str(index + 1) + " from the dataset file " + DATASET_PATH + ": " + statement)
        csv_row = [str(index + 1), "\"" + statement + "\"", DATASET_PATH.split("/")[-2]]
        f.write("[{} - Statement]\n".format(index + 1) + statement +  '\n')

        # Add the urls into embeddings
        tick = time.time()
   
        if len(reports[index]) == 0:
            print("[WARNING] No relevant articles can be found from Google, skipped this statement...")
            continue
        print("[INFO] Spliting articles into chunks...")
            
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        #text_splitter=CharacterTextSplitter(chunk_size=250, chunk_overlap=0)
        all_splits = text_splitter.create_documents(reports[index])

        print("[INFO] Adding " + str(len(all_splits)) +" chunks into the vector store...")
        if USE_PERSIST_DB:
            vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed, persist_directory=CHROMA_PERSIST_DIR)
        else:
            vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

        elapsed_time = time.time() - tick  
        print("[INFO] >>> Finished converting " + str(len(reports[index])) + " documents into the embedding. Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
        f.write("\n[{} - RAG]\n".format(index + 1) + "Finished converting " + str(len(reports[index])) + " documents into the embedding.")
        f.write("Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
        csv_row.append(str(elapsed_time))

        print("[INFO] >>> The total number of documents in vector store is " + str(len(vectorstore.get()['documents'])))

        # LLM Justification
        tick = time.time()
        question = prompt_templates.question_ver_8.format(statement=statement)
            
        qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
        res = qachain.invoke({"query": question})
        print("[INFO] " + color.BOLD + color.CYAN + statement + color.END)
        print("[INFO] " + color.BOLD + color.GREEN + res['result'].strip() + color.END)
        formatted_res = str(res['result']).strip().replace('\n\n', '\n')

        f.write("\n[{} - Response]\n".format(index + 1) + formatted_res + '\n')
        csv_row.append(formatted_res.replace('"', '""').replace("\n", " "))

        elapsed_time = time.time() - tick    
        print("[INFO] >>> Query ended. Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
        f.write("\nElapsed time: "+ "{:.2f}".format(elapsed_time) + "s\n\n")
        csv_row.append(str(elapsed_time))
        csv_all_rows.append(csv_row)

        doc_ids = vectorstore.get()['ids']
        vectorstore.delete(ids=doc_ids)
        print("[INFO] >>> The temporary Chrome DB has been cleared."+ "\n")
        time.sleep(1.5)

fields = ['No', 'Statement', 'Source', 'RAG Time', 'Response', 'Response Time']
with open(output_csv_name, 'w+', encoding='utf8') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    # writing the dataset path for reference purposes
    csvwriter.writerow([DATASET_PATH])
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(csv_all_rows)

if len(dict_statement_reference.keys()) > 0:
    # If json files already exist (there are some statements processed previously), we will append the newly added statement-urls pair(s) into the json files.
    if (len(existing_dict_reference.keys()) > 0):
        with open(statement_urls_dataset_file_name, encoding='utf8') as existing_file:
            existing_dict = json.load(existing_file)
            dict_statement_reference.update(existing_dict)
    
        with open(statement_hash_dataset_file_name, encoding='utf8') as existing_file:
            existing_dict = json.load(existing_file)
            dict_statement_hash.update(existing_dict)

    json.dump(dict_statement_reference, open(statement_urls_dataset_file_name, 'w+'), ensure_ascii=False, indent=4)
    json.dump(dict_statement_hash, open(statement_hash_dataset_file_name, 'w+'), ensure_ascii=False, indent=4)

# Physically remove the chroma database
if USE_PERSIST_DB:
    shutil.rmtree(CHROMA_PERSIST_DIR)
