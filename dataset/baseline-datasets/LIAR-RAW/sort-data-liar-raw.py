import os
import json

# The distribution of labels is LIAR-RAW test set is
# 'true': 205, 
# 'half-true': 263, 
# 'pants-fire': 86,
# 'barely-true': 210, 
# 'mostly-true': 238, 
# 'false': 238, 

dict_stat_labels = {}
dict_claims_by_labels = {}

with open("test.json") as f:
    list_claim_dicts = json.load(f)
    print("[INFO] " + str(len(list_claim_dicts)) + " claims found in LIAR-RAW test set.")
    for d in list_claim_dicts:
        label = d['label']
        if label in dict_stat_labels:
            dict_stat_labels[label] += 1
        else:
            dict_stat_labels[label] = 1
        if label.lower() in ['true', 'false', 'barely-true', 'pants-fire', 'half-true']:
            print("[" + label + "] " + d['claim'])
            reports = []
            if 'reports' in d.keys():
                for rpt in d['reports']:
                    reports.append(rpt['content'].strip().replace('\n', ' '))
            entry = {}
            entry['claim'] = d['claim']
            entry['reports'] = reports
            if label in dict_claims_by_labels:
                dict_claims_by_labels[label].append(entry)
            else:
                dict_claims_by_labels[label] = [entry]

#print(dict_stat_labels)
#print(dict_claims_by_labels)

for output_fn in dict_claims_by_labels.keys():
    f = open(output_fn + ".txt", "w")
    for entry in dict_claims_by_labels[output_fn]:
        f.write(entry['claim'] + "\n")
        for rpt in entry['reports']:
            f.write("*" * 5 + " " + rpt + "\n")
      
    print("[INFO] " + str(len(dict_claims_by_labels[output_fn])) + " claims have been written in file named " + output_fn + ".txt")
    f.close()
    
print("[INFO] All task completed!")
