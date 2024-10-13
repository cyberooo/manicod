import os
import json

# The distribution of labels is FEVER set is
# 'true': 41, 
# 'false': 101, 

dict_stat_labels = {}
dict_claims_by_labels = {}

with open("fever-raw.json") as f:
    all_contents = json.load(f)
    raw_claims = all_contents['examples']
    print("[INFO] " + str(len(raw_claims)) + " claims found in FEVER data set.")
    for d in raw_claims:
        label = 'true' if d['target_scores']['true'] else 'false'
        if label in dict_stat_labels:
            dict_stat_labels[label] += 1
        else:
            dict_stat_labels[label] = 1
        if label.lower() in ['true', 'false']:
            claim_raw = d['input']
            claim = claim_raw.split("claim was made: ")[-1]
            claim = claim.split("\nQ:")[0]
            print("[" + label + "] " + claim)
            if label in dict_claims_by_labels:
                dict_claims_by_labels[label].append(claim)
            else:
                dict_claims_by_labels[label] = [claim]

#print(dict_stat_labels)
#print(dict_claims_by_labels)

for output_fn in dict_claims_by_labels.keys():
    f = open(output_fn + ".txt", "w")
    for claim in dict_claims_by_labels[output_fn]:
        f.write(claim + "\n")
    print("[INFO] " + str(len(dict_claims_by_labels[output_fn])) + " claims have been written in file named " + output_fn + ".txt")
    f.close()
    
print("[INFO] All task completed!")
