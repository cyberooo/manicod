from datetime import datetime

import csv, json, hashlib  
from pathlib import Path

import os
cwd = os.getcwd()
print(cwd)

statement_hash_dataset_file_name = cwd + "/data/statement_database.json"
statement_urls_dataset_file_name = cwd + "/data/url_database.json"

all_statement_hashs_to_keep = []
all_urls_to_delete = []
all_url_hash_to_keep = []
existing_dict_urls = {}



statement_hash_dataset = Path(statement_hash_dataset_file_name)
if statement_hash_dataset.exists():
    existing_dict_statements = json.load(open(statement_hash_dataset_file_name))
    print(">>> Found " + str(len(existing_dict_statements.keys())) + " statement-URLs pair(s) from local storage")
    for key, value in existing_dict_statements.items():
        all_statement_hashs_to_keep.append(value)
else:
    print("Statement list file does not exist.")


statement_urls_dataset = Path(statement_urls_dataset_file_name)
if os.path.exists(statement_urls_dataset):
    with open(statement_urls_dataset, "r") as json_file:
        existing_dict_urls = json.load(json_file)
        hash_to_delete = []
        for key, value in existing_dict_urls.items():
            if key not in all_statement_hashs_to_keep:
                hash_to_delete.append(key)
                for url in value:
                    all_urls_to_delete.append(url)
            else:
                for url in value:
                    url_hash = hashlib.md5(url.encode()).hexdigest()
                    all_url_hash_to_keep.append(url_hash)
        for hash in hash_to_delete:
            del existing_dict_urls[hash]
        print(">>> " + str(len(hash_to_delete)) + " statement records to be deleted from the statement-URL dataset.")
    with open(statement_urls_dataset, "w") as json_file:
        json.dump(existing_dict_urls, json_file, ensure_ascii=False, indent=4)
else:
    print("URL list file does not exist.")

print(">>> " + str(len(all_urls_to_delete)) + " snapshot files to be deleted according to the update of json files.")

for url_to_delete in all_urls_to_delete:
    filename_to_delete = hashlib.md5(url_to_delete.encode()).hexdigest()
    file_path = cwd + '/data/snapshots/' + filename_to_delete
    os.remove(file_path)

num_snapshot_to_del_if_not_exist_in_dataset = 0
for filename in os.listdir(cwd + "/data/snapshots/"):
    if filename not in all_url_hash_to_keep:
        file_path = cwd + '/data/snapshots/' + filename
        os.remove(file_path)
        num_snapshot_to_del_if_not_exist_in_dataset += 1

print(">>> " + str(num_snapshot_to_del_if_not_exist_in_dataset) + " snapshot files deleted as no record found in json files.")