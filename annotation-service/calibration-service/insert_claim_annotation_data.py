import shelve
import re
import sys
import os
import csv
import pickle
import random
import json


MAX_SAMPLES_TABLE = 4 # 5000
MAX_TABLE_SIZE = 50
MIN_TABLE_SIZE = 5
MIN_SENTENCE_LENGTH = 5
# MAX_SAMPLES_TABLE_PER_PAGE = 1

MAX_SAMPLES_SENTENCES = 5 # 2500 (its -1 really)

def generate_manipulation():
    manipulation_list = ['More Specific', 'Generalization', 'Negation', 'Paraphrasing', 'Substitution'] #Multiple Pages

    claim_type = ['First claim', 'Second claim']

    selection_manipulation = random.choices(manipulation_list, weights=(15, 15, 30, 10, 30), k=1)

    selection_claim = random.choice(claim_type)

    manipulation = selection_claim + ': ' + selection_manipulation[0]

    return manipulation


def generate_multiple_pages():
    manipulation_list = [0, 1]

    selection_manipulation = random.choices(manipulation_list, weights=(50, 50), k=1)

    return selection_manipulation[0]

def read_json_tables(path, limit = 100, ratio = 0.7):
    limit_tables = int(limit * ratio)
    limit_infoboxes = int(limit * (1-ratio))
    content_table = {}
    content_infoboxes = {}
    count_tables = 0
    count_infoboxes = 0

    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if  file.endswith(".json"):
                file_paths.append(os.path.join(root,file))

    count_per_file_table = int(limit_tables)#/int(len(file_paths) / 50)) # Use multiple jsons to ensure diversity
    count_per_file_infobox = int(limit_infoboxes)#/int(len(file_paths) / 50)) # Use multiple jsons to ensure diversity

    for file in file_paths:
        # print(file)
        with open(file) as json_file:
            data = json.load(json_file)
            for title in data:
                content_keys = list(data[title].keys())
                random.shuffle(content_keys)
                for key in content_keys:
                    if 'table' in key and data[title][key]['type'] == 'general' and count_tables < limit_tables and len(data[title][key]['table']) >= MIN_TABLE_SIZE and len(data[title][key]['table']) <= MAX_TABLE_SIZE:
                        # print(len([1 for el in content_keys if 'type' in data[title][el] and 'infobox' in data[title][el]['type'] and int(el.split('_')[-1]) < int(key.split('_')[-1])]))
                        content_table['{}_table_general_{}'.format(title, key.split('_')[-1]).replace("'", "''")] = [data[title][key]['table'], title, key]
                        count_tables +=1
                        break
                    elif 'table' in key and data[title][key]['type'] == 'infobox' and count_infoboxes < limit_infoboxes and len(data[title][key]['table']) >= MIN_TABLE_SIZE and len(data[title][key]['table']) <= MAX_TABLE_SIZE:
                        content_infoboxes['{}_table_infobox_{}'.format(title, key.split('_')[-1]).replace("'", "''")] = [data[title][key]['table'],title, key]
                        count_infoboxes+=1
                        break
                if  count_tables % count_per_file_table == 0 and count_infoboxes %  count_per_file_infobox == 0:
                    break
            if count_infoboxes >= limit_infoboxes and count_tables >= limit_tables:
                break

    tables = {**content_table, **content_infoboxes}
    keys =  list(tables.keys())      # Python 3; use keys = d.keys() in Python 2
    random.shuffle(keys)
    tables = dict([(key, tables[key]) for key in keys])

    return tables



def read_json_sentences(path, limit = 100):
    highlight_range = 4
    content= {}
    count_samples = 0

    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if  file.endswith(".json"):
                file_paths.append(os.path.join(root,file))

    count_per_file = int(limit)#/int(len(file_paths) / 50)) # Use multiple jsons to ensure diversity

    for file in file_paths:
        # print(file)
        with open(file) as json_file:
            data = json.load(json_file)
            for title in data:
                order = data[title]['order']
                content_keys = list(data[title].keys())
                sentence_keys = [key for key in content_keys if 'sentence' in key]

                if len(sentence_keys) == 0:
                    continue

                start_index = random.randint(0, int(len(sentence_keys) / 2))
                index_order = order.index(sentence_keys[start_index])

                current_conseq = 0
                current_sentences = []
                for i in range(index_order, len(order)):
                    if 'sentence' in order[i] and len(data[title][order[i]].split(' ')) > MIN_SENTENCE_LENGTH:
                        current_conseq +=1
                        current_sentences.append(order[i])
                        if current_conseq == highlight_range:
                            break
                    else:
                        current_conseq = 0
                        current_sentences = []
                if current_conseq < highlight_range:
                    continue
                else:
                    content['{}'.format(title).replace("'", "''")] = []
                    for key in current_sentences:
                        content['{}'.format(title).replace("'", "''")].append([data[title][key], title, key])
                    count_samples+=1
                if count_samples % count_per_file == 0:
                    break
            if count_samples >= limit:
                break

    keys =  list(content.keys())
    random.shuffle(keys)
    sentence_highlights = dict([(key, content[key]) for key in keys])

    return sentence_highlights


def table_claim_data():
    #Not possible to detect exact table, since they all use some heuristics to determine table etc. However, can be sure that table is not in set by excluding tables from that entire page. (e.g. when training on our data and testing on theirs to see how additional supervision affects scores)
    ott_set_ini= pickle.load(open("../related_data/ott_table_ids_extracted", "rb" ) )
    tabfacts1_id, tabfacts1_section = pickle.load( open( "../related_data/tabfacts1_table_ids_extracted", "rb" ) )
    tabfacts2_id, tabfacts2_section = pickle.load( open( "../related_data/tabfacts2_table_ids_extracted", "rb" ) )

    ott_set = set([])
    for el in list(ott_set_ini):
        ott_set.add(' '.join(el.split('_')[:-1]))
    title_ids_f = open('/srv/data/title_ids.txt', 'r')
    title_ids = {}
    for l in title_ids_f.readlines():
        title, id = l.strip().split('\t')
        title_ids[title] = id

    output_query = []

    tables = read_json_tables('/srv/data/wiki_full_new/wiki-pages', limit = MAX_SAMPLES_TABLE)


    table_ids = []
    titles = []
    page_ids = []
    all_hyperlinks = []
    in_tabfacts1 = []
    in_tabfacts2 = []
    in_ott = []

    for tab in tables:
        content, title, key = tables[tab]
        table_ids.append(tab)
        titles.append(title.replace("'", "''"))
        page_id = title_ids[title] if title in title_ids and title_ids[title] != 'None' else 0
        page_ids.append(page_id)
        in_tabfacts1.append(1 if page_id in tabfacts1_id else 0)
        in_tabfacts2.append(1 if page_id in tabfacts2_id else 0)
        in_ott.append(1 if title in ott_set else 0)
        hyperlinks = []
        for row in content:
            for cell in row:
                match = re.findall('\[\[(.+?)\|(.+?)\]\]', cell['value'])
                if len(match) > 0 and len(hyperlinks) < 30:
                    hyperlinks.append(' [SEP] '.join([ele[0].replace("'", "''") for ele in match]))
        all_hyperlinks.append(' [SEP] '.join(hyperlinks))

    # print(in_ott)
    # print(in_tabfacts1)
    # with open('check.txt', 'w') as f:

    for i in range(len(table_ids)):

            # f.write("INSERT INTO  ClaimAnnotationData(page, page_id, is_table, selected_id, manipulation, quick_hyperlinks, taken_flag, annotators_num, in_tabfacts1, in_tabfacts2, in_ott, skipped, skipped_by) VALUES ('{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});\n".format(titles[i], page_ids[i], 1, table_ids[i],  generate_manipulation(), all_hyperlinks[i], 0, 0, in_tabfacts1[i], in_tabfacts2[i], in_ott[i], 0, 0))

        output_query.append("INSERT INTO  CalibrationClaimAnnotationData(page, page_id, is_table, selected_id, manipulation, quick_hyperlinks, taken_flag, annotators_num, in_tabfacts1, in_tabfacts2, in_ott, skipped, skipped_by, multiple_pages) VALUES ( '{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {});\n".format(titles[i], page_ids[i], 1, table_ids[i],  generate_manipulation(), all_hyperlinks[i], 0, 0, in_tabfacts1[i], in_tabfacts2[i], in_ott[i], 0, 0, generate_multiple_pages()))

    # print('Table highlights addded', len(output_query))
    return output_query

def sentence_claim_data():

    title_ids_f = open('/srv/data/title_ids.txt', 'r')
    title_ids = {}
    for l in title_ids_f.readlines():
        title, id = l.strip().split('\t')
        # if title == None:
        #     print(title, id)
        title_ids[title] = id

    output_query = []

    sentences = read_json_sentences('/srv/data/wiki_full_new/wiki-pages', limit = MAX_SAMPLES_SENTENCES)

    sentence_ids = []
    titles = []
    page_ids = []
    all_hyperlinks = []

    for highlight in sentences:
        titles.append(highlight)
        page_ids.append(title_ids[highlight.replace("''", "'")] if highlight.replace("''", "'") in title_ids and title_ids[highlight.replace("''", "'")] != 'None' else 0)
        id_concat = []
        hyperlinks = []
        for cont in sentences[highlight]:
            sentence, title, id = cont
            id_concat.append(highlight + '_' + id)
            hyperlink = re.findall('\[\[(.+?)\|(.+?)\]\]', sentence)
            hyperlinks += hyperlink
        sentence_ids.append(' [SEP] '.join(id_concat).replace("'", "''"))
        all_hyperlinks.append(' [SEP] '.join(ele[0] for ele in hyperlinks).replace("'", "''"))

    # print(page_ids)



    # with open('check.txt', 'w') as f:
    for i in range(len(sentence_ids)):
            # f.write("INSERT INTO  ClaimAnnotationData( page, page_id, is_table, selected_id, manipulation, quick_hyperlinks, taken_flag, annotators_num, in_tabfacts1, in_tabfacts2, in_ott, skipped, skipped_by) VALUES ('{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});\n".format( titles[i], page_ids[i], 0, sentence_ids[i],  generate_manipulation(), all_hyperlinks[i], 0, 0, 0, 0, 0, 0, 0))
        output_query.append("INSERT INTO  CalibrationClaimAnnotationData( page, page_id, is_table, selected_id, manipulation, quick_hyperlinks, taken_flag, annotators_num, in_tabfacts1, in_tabfacts2, in_ott, skipped, skipped_by, multiple_pages) VALUES ('{}', {}, {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {}, {});\n".format(titles[i], page_ids[i], 0, sentence_ids[i],  generate_manipulation(), all_hyperlinks[i], 0, 0, 0, 0, 0, 0, 0, generate_multiple_pages()))

    # print('Sentence highlights', len(output_query))
    return output_query

if __name__ == '__main__':
    outputs = []
    outputs += table_claim_data()
    outputs += sentence_claim_data()
    random.shuffle(outputs)
    with open('check.txt', 'w') as f:
        for entry in outputs:
            f.write(entry)
            print(entry)
