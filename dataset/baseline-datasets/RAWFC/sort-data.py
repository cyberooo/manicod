import os
import json

# The distribution of labels is RAWFC test set is
# 'false': 53, 
# 'Mostly False': 12, 
# 'misattributed': 1, 
# 'mixture': 49, 
# 'true': 47, 
# 'correct attribution': 12, 
# 'unproven': 18, 
# 'Mostly True': 8

files = [f for f in os.listdir('.') if (os.path.isfile(f) and f.endswith('.json'))]
print("[INFO] " + str(len(files)) + " JSON files found in the RAWFC test dataset.")

dict_stat_labels = {}
dict_claims_by_labels = {}

for fn in files:
    print("[INFO] Processing JSON file: " + fn, end=" ")
    with open(fn) as f:
        d = json.load(f)
        label = d['label']
        #print(d['original_label'])
        if label in dict_stat_labels:
            dict_stat_labels[label] += 1
        else:
            dict_stat_labels[label] = 1
        if label.lower() in ['true', 'false', 'half']:
            print("[" + label + "] " + d['claim'])
            if label in dict_claims_by_labels:
                dict_claims_by_labels[label].append(d['claim'])
            else:
                dict_claims_by_labels[label] = [d['claim']]
        else:
            print("skipped due to non-binary label.")

#print(dict_stat_labels)
#print(dict_claims_by_labels)

for output_fn in dict_claims_by_labels.keys():
    f = open(output_fn + ".txt", "w")
    for claim in dict_claims_by_labels[output_fn]:
        f.write(claim + "\n")
    print("[INFO] " + str(len(dict_claims_by_labels[output_fn])) + " claims have been written in file named " + output_fn + ".txt")
    f.close()
    
print("[INFO] All task completed!")