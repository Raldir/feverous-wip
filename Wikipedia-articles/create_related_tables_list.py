import re
import sys
import os
import json
import pickle

def create_list_totto():
    with open('../../Related_Data/totto_data/totto_train_data.jsonl', 'r') as json_file:
        json_list = list(json_file)

    with open('totto_table_ids_extracted', 'w') as f:
        for json_str in json_list:
            result = json.loads(json_str)
            #print("result: {}".format(result))
            f.write('{}\t{}\t{}\n'.format(result['table_page_title'], result['table_section_title'], result['table_section_text']))

def create_list_tabfacts1():
    tabfacts_id = []
    tabfacts_section = []
    with open('../../Related_Data/TabFacts/r1_training_all.json', 'r') as json_file:
        tabfacts_dict = json.loads(json_file.read())
        for entry in tabfacts_dict:
            entry_parts = entry.split('-')
            tabfacts_id.append(entry_parts[1])
            tabfacts_section.append(entry_parts[2].split('.')[0])
    pickle.dump((tabfacts_id, tabfacts_section), open('tabfacts1_table_ids_extracted', 'wb'))

def create_list_tabfacts2():
    tabfacts_id = []
    tabfacts_section = []
    with open('../../Related_Data/TabFacts/r2_training_all.json', 'r') as json_file:
        tabfacts_dict = json.loads(json_file.read())
        for entry in tabfacts_dict:
            entry_parts = entry.split('-')
            tabfacts_id.append(entry_parts[1])
            tabfacts_section.append(entry_parts[2].split('.')[0])
    pickle.dump((tabfacts_id, tabfacts_section), open('tabfacts2_table_ids_extracted', 'wb'))



def create_list_ott_qa():
    ott_set = set([])
    with open('../../Related_Data/OTT-QA/train.json', 'r') as json_file:
        ott_dict = json.loads(json_file.read())
        for entry in ott_dict:
            ott_set.add(entry['table_id'])
    pickle.dump(ott_set, open('ott_table_ids_extracted', 'wb'))

    # for json_str in json_list:
    #     result = json.loads(json_str)
    #     print("result: {}".format(result))
        # with open('totto_table_ids_extracted', 'w') as f:
        #     f.write('{}\t{}\t{}'.format(result['table_page_title'], result['table_section_title'], result['table_section_text']))

#create_list_totto()
create_list_tabfacts1()
create_list_tabfacts2()
create_list_ott_qa()
