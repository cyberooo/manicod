#!/usr/bin/env python

from datetime import datetime
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from utils.console_format import color
from utils.gen_date_range_for_google_search import generate_tbs_param
import utils.prompt_templates as prompt_templates
import utils.extract_from_url as extract_from_url
from utils.google_search_api import GoogleAPIModel
from pathlib import Path
import time
import sys
import shutil
import ssl
import csv
import json
import hashlib
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

USE_PERSIST_DB = False

API = GoogleAPIModel(verbose=True)
# Set default dataset and model to use

MODEL = 'llama3.1:8b-instruct-fp16'

CWD = os.getcwd()

DATASET_PATH = os.path.join(CWD, 'dataset/final-datasets/news_index_20240724.json')

if (len(sys.argv) > 1):
    if (sys.argv[1]):
        MODEL = sys.argv[1]
    if (sys.argv[2]):
        DATASET_PATH = sys.argv[2]

print("[INFO] You're using " + MODEL + " model now")

time_str = datetime.now().strftime('%Y-%m-%d-%H%M%S')

CHROMA_PERSIST_DIR = "./chroma_db_" + time_str

data_set_file_str = DATASET_PATH.split("/")[-1].split(".json")[0]
data_set_date_str = data_set_file_str.split("_")[-1]

output_file_path = os.path.join(CWD, "logs/log_" + time_str + "_"  + data_set_file_str + ".log")
output_csv_path = os.path.join(CWD, "logs/log_" + time_str + "_"  + data_set_file_str + ".csv")
statement_hash_dataset_file_path = os.path.join(CWD, "data/statement_database.json")
statement_urls_dataset_file_path = os.path.join(CWD, "data/url_database.json")
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

statement_urls_dataset = Path(statement_urls_dataset_file_path)
if statement_urls_dataset.exists():
    existing_dict_reference = json.load(open(statement_urls_dataset_file_path))
    print("[INFO] >>> Found " + str(len(existing_dict_reference.keys())) + " statement-URLs pair(s) from local storage")
else:
    existing_dict_reference = {}

dataset = json.load(open(DATASET_PATH))
statements = []
statement_digests = []
domains = []
google_gl_countries = []
news_source = []
for news_digest in dataset.keys():
    statements.append(dataset[news_digest]['text'])
    news_source.append(dataset[news_digest]['source'])
    # Select the optimal domain for news search
    news_domain = "google.com"
    gl_country = "us"
    if 'source' in dataset[news_digest].keys():
        if 'bbc' in dataset[news_digest]['source'] or '_uk' in dataset[news_digest]['source'] or \
            'BBC' in dataset[news_digest]['source'] or 'UK' in dataset[news_digest]['source']:
            news_domain = "google.co.uk"
            gl_country = "uk"
        elif 'cna' in dataset[news_digest]['source'] or '_sg' in dataset[news_digest]['source'] or \
                'CNA' in dataset[news_digest]['source'] or 'Singapore' in dataset[news_digest]['source']:
            news_domain = "google.com.sg"
            gl_country = "sg"
        elif '_ca' in dataset[news_digest]['source'] or 'Canada' in dataset[news_digest]['source']:
            news_domain = "google.ca"
            gl_country = "ca"
        elif '_au' in dataset[news_digest]['source'] or 'Australia' in dataset[news_digest]['source']:
            news_domain = "google.com.au"
            gl_country = "au"
        elif '_nz' in dataset[news_digest]['source'] or 'New Zealand' in dataset[news_digest]['source']:
            news_domain = "google.co.nz"
            gl_country = "nz"
        elif '_za' in dataset[news_digest]['source'] or 'South Africa' in dataset[news_digest]['source']:
            news_domain = "google.co.za"
            gl_country = "za"
    domains.append(news_domain)
    google_gl_countries.append(gl_country)
    statement_digests.append(dataset[news_digest]['digest'])

print("[INFO] " + str(len(statements)) + " statements loaded...")

with open(output_file_path,"a+", encoding='utf8') as f:
    for index, statement in enumerate(statements):
        
        print("[INFO] Inferring statement no." + str(index + 1) + " from the dataset file " + data_set_file_str + ": " + statement)
        csv_row = [str(index + 1), "\"" + statement + "\"", news_source[index]]
        f.write("[{} - Statement]\n".format(index + 1) + statement +  '\n')

        statement_hash = hashlib.md5(statement.encode()).hexdigest()
        # Use the digest from dataset to avoid searching Google, need to be careful as the original searched result may not always work for fake news detection!
        #statement_hash = statement_digests[index]

        try:
            if statement_hash in existing_dict_reference.keys():
                urls = existing_dict_reference[statement_hash]['urls']
                titles = existing_dict_reference[statement_hash]['titles']
                snippets = existing_dict_reference[statement_hash]['snippets']
                dates = existing_dict_reference[statement_hash]['dates']
                print('[INFO] The statement has been processed previously, loading URLs from local storage' )
                #print(urls)
                f.write("\n[{} - Search results]\n".format(index + 1))
                for i in range(0, len(urls)):
                    f.write('[URL from local storage]\n' + str(titles[i]) + '\n' + str(urls[i]) + '\n')

            else:
                print('[INFO] Searching "' + statement + '" on Google side ' + domains[index] + ' (country code: ' + google_gl_countries[index] +')')
                # Directly using the GoogleAPIModel to retrieve top a few urls
                tbs_param = generate_tbs_param(data_set_date_str, delay_days=1)
                urls, titles, snippets, dates = API.serpapi_google_search(statement, num_responses=5, 
                                                                          google_domain=domains[index], 
                                                                          gl_country=google_gl_countries[index],
                                                                          tbs=tbs_param)
            
                #print(urls)
                f.write("\n[{} - Search results]\n".format(index + 1))
                for i in range(0, len(urls)):
                    f.write(str(titles[i]) + '\n' + str(urls[i]) + '\n')
                
                dict_statement_hash[statement] = statement_hash

                statement_reference = {}
                statement_reference['urls'] = urls
                statement_reference['titles'] = titles
                statement_reference['snippets'] = snippets
                statement_reference['dates'] = dates
                dict_statement_reference[statement_hash] = statement_reference
                # print(statement_reference)

            # Add the urls into embeddings
            tick = time.time()
            articles = []
            for url_index, url in enumerate(urls):
                curr_article_text = ""
                try:
                    url_hash = hashlib.md5(url.encode()).hexdigest()
                    article_offline_file = Path(os.path.join(CWD, 'data/snapshots/' +  url_hash))
                    if article_offline_file.exists():
                        print("[INFO] The article of given URL has been snapshot earlier, reading from local storage...")
                        with open(os.path.join(CWD, 'data/snapshots/' +  url_hash), 'r', encoding='utf8') as file:
                            curr_article_text = file.read()
                    else:
                        curr_article_text = extract_from_url.get_text(url, title=titles[url_index], snippet=snippets[url_index])   

                        with open(os.path.join(CWD, 'data/snapshots/' +  url_hash), 'w+', encoding='utf8') as file:
                            # We are going to write the title, snippet, date, and content of the webpage into the snapshot file
                            file.write(titles[url_index] + '\n' + snippets[url_index] + '\n')
                            if dates[url_index] != '':
                                file.write('Posted on ' + dates[url_index] + '.\n')
                            file.write(curr_article_text)
                    articles.append(curr_article_text)

                except Exception as error:
                    # handle the exception
                    print("[ERROR] An exception occurred:", error) 
                    f.write("!! An exception occurred, skipped.\n" + str(error) + "\n")
            if len(articles) == 0:
                print("[WARNING] No relevant articles can be found from Google, skipped this statement...")
                continue
            print("[INFO] Spliting articles into chunks...")
            
            text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            
            all_splits = text_splitter.create_documents(articles)

            print("[INFO] Adding " + str(len(all_splits)) +" chunks into the vector store...")
            if USE_PERSIST_DB:
                vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed, persist_directory=CHROMA_PERSIST_DIR)
            else:
                vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

            elapsed_time = time.time() - tick  
            print("[INFO] >>> Finished converting " + str(len(urls)) + " documents into the embedding. Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
            f.write("\n[{} - RAG]\n".format(index + 1) + "Finished converting " + str(len(urls)) + " documents into the embedding.")
            f.write("Elapsed time: "+ "{:.2f}".format(elapsed_time) + "s")
            csv_row.append(str(elapsed_time))

            print("[INFO] >>> The total number of documents in vector store is " + str(len(vectorstore.get()['documents'])))

            # LLM Justification
            tick = time.time()
            question = prompt_templates.question_ver_9.format(statement=statement)
            
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

        except Exception as error:
            # handle the exception
            print("[ERROR] An exception occurred:", error,"\n\n") 
            f.write("!! An exception occurred, skipped.\n" + str(error) + "\n")

fields = ['No', 'Statement', 'Source', 'RAG Time', 'Response', 'Response Time']
with open(output_csv_path, 'w+', encoding='utf8') as csvfile:
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
        with open(statement_urls_dataset_file_path, encoding='utf8') as existing_file:
            existing_dict = json.load(existing_file)
            dict_statement_reference.update(existing_dict)
    
        with open(statement_hash_dataset_file_path, encoding='utf8') as existing_file:
            existing_dict = json.load(existing_file)
            dict_statement_hash.update(existing_dict)

    json.dump(dict_statement_reference, open(statement_urls_dataset_file_path, 'w+'), ensure_ascii=False, indent=4)
    json.dump(dict_statement_hash, open(statement_hash_dataset_file_path, 'w+'), ensure_ascii=False, indent=4)

# Physically remove the chroma database
if USE_PERSIST_DB:
    shutil.rmtree(CHROMA_PERSIST_DIR)
