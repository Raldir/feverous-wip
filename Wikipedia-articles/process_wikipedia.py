# from html.parser import HTMLParser
# from urllib.request import urlopen
# from lxml.html import parse
#
# class MyParser(HTMLParser):
#     def __init__(self, *args, **kwargs):
#         self.results = []
#         super(MyParser, self).__init__(*args, **kwargs)
#         def handle_starttag(self, tag, attrs):
#             if tag == "td":
#                 for attr, value in attrs:
#                     if ("colspan" == attr) or ("rowspan" == attr):
#                         self.results.append("{}=\"{}\"".format(attr, value))
#
# parsed = parse(urlopen('https://en.wikipedia.org/wiki/Ken_Fujita'))
# doc = parsed.getroot()
# tables = doc.findall('.//table')
# parser = MyParser(doc)
# parser.feed()


"""
Extraction notes:
Some tables are not extracted due to errors on Wikipedia side: Users specify wrong column/row span (sometimes too long since Wikipedia simply ignores spans that are longer than min span) or have typos.
"""
import re
import copy

from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml.html import parse
import sys
from bs4 import BeautifulSoup, NavigableString, CData, Tag
import nltk
from tqdm import tqdm
extra_abbreviations = list(set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'e.g', 'eg', 'ie', 'c.f', 'b.c.e', 'pg', 'm.a', 'd.c', 'gen', 'cb', 'h.g', 'å', 'ms', 'col', 'mr', 'bros', 'lbf', 'mc', 'jr', 'rep', 'gcs', 'µci', 'op', 'vol', 'pot', 'mya', 'w.e.b', 'c.e', 'est', 'l.c', 'maj', 'o.b', 'e.t.a', 'sp', 'bi', 'a.m.i', 'r', 'pp', 'verified', 'pl', 'g.a.t.c', 'o.k', 'igo', '|mr', 'u.n', 'zrn', 'n.v', 'w', 'dr', 'inc', 'e.g', 'sr', 'a23', 'a.d', 'f.o', '−δh', 'ca', 'w.c', 'f.c', 'sen', 'u.s.n', 'rt', 'fl', 'e.w', 'd.a.b.t', 'b.c', 'msc', 'mrs', 'u.s', 'u.k', 's.p.a', 'a.m', 'u.s', 'o.m', 'c', 'corp', 'n.o.i.f', 'spp', 'p.m', 'cir', 'rig', 'u.s.c', 'ypb', 's.a', 'b.v', 'i.e', 'etc', 'c.f.r', 'hon', 'a.c', 'hist', 'd.r', 'stb', 'bros', 'i.a.s', 'vid', 'w', 't.n', 'p.r', 'lat', 'katczinsky', 'w.h', 'e.i', 'p.m', 'epist', 'sanh', 'g.f', 'd.sc', 'u.k', 'khm', 'a.i', 'xxxii', 'ān-', 'xli', 'm.e', 'aδ', 't.c.w', 'ypb', 'p.e.i', 'e.n.e', 's.m', 'b.a', '1/b', 'sr', 'low—i.e', 'const', 'd.m', '|st', 'uts', 'o.t.o', 'în', 'f4v', 'b.p', 'h.g.h', 'n.e', 'h.q', '|mr', 'c.j', 'u.s.a', 'en-', 'j.d', 'f.m', 'd.l', 'ros', 'm.i', 'j.p', 'ka3', 'grs', 'c.s.c', 'n.c', 'vol', 'unrest——viz', 'f.c', 'w.c', "'w", 'm.d', 'a.b.c', '|a.g', 'tosef', 'libr', "'u.s", 'k.p', 'w.e.b', 'adv', 'f.j', '|s', 'g.a.t.c', 'c18', 'deut', 'emph', 'h.t', '|ms', 'a.h', 'u.n', 'j.b.a', '97p', 'nov', 'c.8', 'udc', 'o.s', 'r.v', 'p.j.h', 'd.l.r', 'mek', 'yer', 'm.s', 'c.i.l', 'ams', 'c95', 'c.f.r', 'f.k', '5%p.a', 'etc', 's.d', 'haer', 'j.j', 's.e', 'j.e', 'hurr', '01h', 'e.g', 'től', 'd.c', 'e.j', 'yeb', 'n.s', 'iba', 'ð̴/', 'z.e', 'u.s.n', 'mk.i', '+n', 'p.c.l', 'u.s.c', '|g.d', '1039ff', 's.r.l', 'o.b', 'e.t', 'a.a', 'św', 'c.w', '2am', 'ibid', 'j', 's.o.s', 'u.c.l.a', 'cir', 'seq', 'lib', 'i.e', 'kla', 'jud', 'y.u.c.k', 'vln', 'aro', 'p.s', '−δh', 'mds', 'p.a', 'c.e', 'ک', 'g.j', 'b.s', 'viz', 'b.i.d', 'r.h', 'o-h', 'n.y', 'syn', 'd.a', 'ḳ', 't.r.e.e', 'eṯ-', 'un-', 'ibs', 'll.d', 'h.a', 'a.m', '.h', 'h.p', 'it”', 'v.d', '|dr', 'e.k', 'j.c', 'rd', 'x=1', 'n−c', 'j.c.a', 'l.a', 's.a.s', 'r.b', '_made_in_america|o.j', 'j.m', 'q.e', 'j.f', 'a.k.a', 'c&a', 's.j', 'a.u', "'o.k", 'ph.d', 'aftermath—i.e', 'p.l', 'ᾰᾰ', 'c.q', 't.h.c', 'eds', 'c.c', 'l.c', 'hdt', '⟨ḍ⟩', 'r–n.m', 'c.f.w', 'soz', 'r.i', 'b.v', 'd.a.b.t', 'v.c', 'j.s', 'm.m', 'de/', 'vols', 'a.l', '—i.e', 'a.g', 'a23', 'boc', 'jr', 'us—i.e', 'p.g', 'o.j', 'bvt', 'a.m.i', 'm.a', 'v.w', 'skt', 's.l', 'jur', 'n.v', '|e.t', 'o.k', 'e.t.a', 'e.w', 'd.o', 'aug', 'a.d', '3.5%p.a', 'ie', 's.c.r', 'k.r', 'esq', 'mic', 'hon', 'sgt', 'a.e', 'o.m', 'rug', 'cfr', 'ωij', 'h.g', 'k.u.k', 'abbrev', 'e.v', 'p2y', 'pl', 'r.w', 'uwf', 'j.-c', 'n.o.i.f', 'nil', '|u.s', 'e.l', '11%p.a', 'i.q', '|l.a', 'jer', 'lúi', 'd.j', 'µci', 't.g.i', 'j/', 'ŉ', 'fr', 'b.c', 't.j', 'e.r', 'kb6', 'bfs', 'abbrv', 'αr', 'c.m', 'v.b', 's.k', 'g.n', 'd.p', 'col', 'gcs', 'c.y', 'b.i.g', 'maj', 'n.w', 'vz', 'p67', 'w.a.c', 'akon', 'a.f', 'a.j.j', 'dimensions—e.g', 'me’', 'l.p', 'f.sh.f', 'c.t', 'h.r', 'l.o', 'zrn', 's.s', 'abbr', 'a.c', 'e.u', 'r.s', 'kmt', 'qeq', 'g.d', '/ŭ/', 'fl', 'f.o', 'c.u', 'smg', 'l.h', 'eccl', 'sct', 'ℤ', '/k/', 'eua', 'a.s', 'coh', 'iex', 'gk', 'july/aug', 'rep', '—e.g', 'resp', 'n.n', '|c.s', 'd2o', 'c.s', 'sm̥', 'b.c.e', 'property—i.e', 'č', 's.p.a']))
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sent_tokenizer._params.abbrev_types.update(extra_abbreviations)
import tarfile
from datetime import datetime
import os
from urllib.parse import unquote
from xml.sax import saxutils
import logging
import json
from multiprocessing.pool import Pool
import time
import shelve
import threading
from os import walk
import multiprocessing
import traceback


class Extractor(object):
    def __init__(self, **kwargs):

        self._transformer = str

    def reset_variables(self):

        self.sentence_id = 0

        self.title = None
        self.id = None

        self.section_id = 0
        self.current_section = 0


        self.table_id = 0
        self.current_table = None
        self.column_num_cell = 0
        self.row_num_cell = 0
        #self.sentence_id_in_table = 0
        self.cell_element = 0

        self.point_id = 0
        self.current_list = None
        self.list_id = 0

        # self.infobox_id = 0


    def dictify(self, ul, parsed_content, data, current_level = 0):
        last_dt = None
        for li in ul.find_all(['li', 'dt', 'dd'], recursive=False):
            if li.get_text() == '':
                continue
            li_text  = self.extract_text(copy.copy(li))
            try:
                key = next(li.stripped_strings)
            except:
                logging.warning('Stopped iteration for list in {}'.format(self.title))
                #traceback.print_exc()
                continue
            ul = li.find(['ul','ol','dl'])
            if ul:
                ul_type = ul.name
                map_type = {'ul' : 'unordered_list', 'ol' : 'ordered_list', 'dl': 'unordered_list'}
                if li.name == 'dt':
                    last_dt = li_text
                    continue
                elif last_dt != None:
                    parsed_content.append('<{}>{}: {}<span style="visibility: hidden;font-size:1px">{}_item_{}_{}</span></{}>'.format('li', last_dt,  li_text, self.title, str(self.current_list), str(self.point_id), 'li'))
                    parsed_content.append('<{}>'.format(ul.name if ul.name != 'dl' else 'ul'))
                    data['list_{}'.format(self.list_id)]['list'].append({'value':'{}: {}'.format(last_dt, li_text), 'level' : current_level,  'type': map_type[ul_type]})
                    self.point_id +=1
                    self.dictify(ul, parsed_content, data, current_level + 1)
                    parsed_content.append('</{}>'.format(ul.name if ul.name != 'dl' else 'ul'))
                    last_dt = None
                else:
                    parsed_content.append('<{}>{}<span style="visibility: hidden;font-size:1px">{}_item_{}_{}</span></{}>'.format('li',  li_text, self.title, str(self.current_list), str(self.point_id), 'li'))
                    parsed_content.append('<{}>'.format(ul.name if ul.name != 'dl' else 'ul'))
                    data['list_{}'.format(self.list_id)]['list'].append({'value' : li_text, 'level' : current_level, 'type': map_type[ul_type]})
                    self.point_id +=1
                    self.dictify(ul, parsed_content, data, current_level + 1)
                    parsed_content.append('</{}>'.format(ul.name if ul.name != 'dl' else 'ul'))
            else:
                if li.name == 'dt':
                    last_dt = li_text
                    continue
                elif last_dt != None:
                    parsed_content.append('<{}>{}: {}<span style="visibility: hidden;font-size:1px">{}_item_{}_{}</span></{}>'.format('li', last_dt,  li_text, self.title, str(self.current_list), str(self.point_id), 'li'))
                    data['list_{}'.format(self.list_id)]['list'].append({'value':li_text, 'level' : current_level})
                    self.point_id +=1
                    last_dt = None
                else:
                    # print(li_text)
                    parsed_content.append('<{}>{}<span style="visibility: hidden;font-size:1px">{}_item_{}_{}</span></{}>'.format('li',  li_text, self.title, str(self.current_list), str(self.point_id), 'li'))
                    data['list_{}'.format(self.list_id)]['list'].append({'value':li_text, 'level' : current_level})
                    self.point_id +=1

    def parse_article(self, doc, title):
        # doc = urlopen(url)
        self.reset_variables()
        self.title = title

        soup = BeautifulSoup(doc, 'lxml')

        body = soup.find("div", {"class": "mw-parser-output"})
        try:
            content = body.findAll(['p', "table", 'ul', 'ol', 'dl', 'h2', 'h3', 'h4', 'h5', 'h6', 'div'], recursive=False) #if isinstance(input, str) else input
        except Exception as inst:
            logging.info('Error in processing body in {}'.format(self.title))
            logging.info(inst)
            #traceback.print_exc()

        excluded_sections = ['References', 'Citations', 'Sources', 'Further reading', 'External links', 'Works', 'Gallery', 'Citations and references', 'Bibliography', 'External links & References', 'Notes and references', 'Notes', 'Notes, citations, and references', 'Notes, references, and citations', 'Citations, notes, and references', 'References, citations, and notes', 'References, notes, and citations', 'Works cited', 'Footnotes']

        parsed_content = []
        data = {'order' : [], 'title': self.title}
        skip_flag = False
        current_section = None
        for i, element in enumerate(content):
            # print(element.name)
            if element.get_text() == '\n':
                continue
            math_img = element.find('img')
            if math_img and math_img.has_attr('class') and len([s for s in math_img.get('class') if 'math' in s]) > 0: # exclude equations
                continue
            elif element.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
                current_section = element.name
                if skip_flag and element.name != skip_flag:
                    continue
                else:
                    section_title = element.find("span", {"class": "mw-headline"}).get_text().strip()
                    section_size = int(element.name[1])
                    skip_flag = False
                    first_section_appeared = True
                    if section_title in excluded_sections:
                        break
                    else:
                        parsed_content.append('{} {} <span style="visibility: hidden;font-size:1px">{}_section_{}</span> {}\n'.format(section_size * '=', section_title, self.title, self.current_section, section_size * '='))
                        data['section_{}'.format(self.current_section)] = section_title
                        data['order'].append('section_{}'.format(self.current_section))
                        self.current_section +=1
                        self.section_id+=1
            elif (element.name == 'p' or (element.name == 'div' and element.has_attr('class') and ['hatnote', 'navigation-not-searchable'] == element.get('class'))) and not skip_flag:
                #print(element)
                text = self.extract_text(element)
                text = text.replace('\n', ' ')
                for tok in  sent_tokenizer.tokenize(text):
                    parsed_content.append(tok + ' <span style="visibility: hidden;font-size:1px">' + self.title + '_sentence_' + str(self.sentence_id) + '</span>\n')
                    data['sentence_{}'.format(self.sentence_id)] = tok
                    data['order'].append('sentence_{}'.format(self.sentence_id))
                    self.sentence_id+=1
            elif element.name == 'table' and element.has_attr('class') and not skip_flag:
                reference_issues = element.find('a', {'href': '/wiki/File:Question_book-new.svg'})
                tab_img = element.find('img')
                reference_issues_2 = tab_img and tab_img.has_attr('src') and ('Ambox_important' in tab_img['src'] or 'Question_book-new' in tab_img['src'] or 'question_mark' in tab_img['src'])
                # if set(["box-Cite_check", "box-Unreferenced", "box-No_footnotes", "box-Multiple_issues"]).intersection(set(element.get('class'))):
                if reference_issues or reference_issues_2:
                    if current_section == None:
                        error_string = 'Article has citation/reference issues. Skip article... {}'.format(self.title)
                        raise RuntimeError(error_string)
                    else:
                        skip_flag = current_section
                elif 'infobox' in element.get('class'):
                    table_caption = element.find("caption")
                    if table_caption:
                        table_caption = self.extract_text(table_caption)
                    try:
                        parsed_table = self.parse_table(element, is_infobox= True)
                        content  = self.convert_table_to_wikidata(parsed_table, table_caption, data, is_infobox = True)
                        parsed_content += content
                    except Exception as inst:
                        logging.warning('Error in processing infobox {}'.format(self.title))
                        logging.warning(inst)
                        #traceback.print_exc()
                elif ('wikitable' in element.get('class')):
                # elif current_section != None:
                    table_caption = element.find("caption")
                    if table_caption:
                        table_caption = self.extract_text(table_caption)
                    try:
                        parsed_table = self.parse_table(element)
                        content = self.convert_table_to_wikidata(parsed_table, table_caption, data)
                        parsed_content+= content
                    except Exception as inst:
                        logging.warning('Error in processing table {}'.format(self.title))
                        logging.warning(inst)
                        #traceback.print_exc()
            # elif element.name == 'div' and element.has_attr('class') and ['hatnote', 'navigation-not-searchable'] == element.get('class'):
            #     print('BABABL', self.extract_text(element))
                #content.append(self.extract_text(element) + '\n')
            elif element.name in ['ul', 'ol', 'dl'] and not skip_flag:
                # if element.find('img'): # Why again?
                #     continue
                if element.name == 'dl':
                    parsed_content.append('<span style="visibility: hidden;font-size:1px">{}_description_list_{}</span>'.format(self.title, self.list_id))
                    data['list_{}'.format(self.list_id)] = {'list': [], 'type': 'description_list'}
                elif element.name == 'ol':
                    parsed_content.append('<span style="visibility: hidden;font-size:1px">{}_ordered_list_{}</span>'.format(self.title, self.list_id))
                    data['list_{}'.format(self.list_id)] = {'list': [], 'type': 'ordered_list'}
                else:
                    parsed_content.append('<span style="visibility: hidden;font-size:1px">{}_unordered_list_{}</span>'.format(self.title, self.list_id))
                    data['list_{}'.format(self.list_id)] = {'list': [], 'type': 'unordered_list'}
                self.current_list = self.list_id
                data['order'].append('list_{}'.format(self.list_id))
                parsed_content.append('<{}>'.format(element.name if element.name != 'dl' else 'ul'))
                lists = self.dictify(element, parsed_content, data)
                parsed_content.append('</{}>'.format(element.name if element.name != 'dl' else 'ul'))
                self.list_id +=1

        parsed_content.append('\n\n<span style="font-size:65%">Credits to the contents of this page go to the authors of the corresponding Wikipedia page: en.wikipedia.org/wiki/{}.</span>'.format(self.title))
        final_out = '\n'.join(parsed_content)

        # print(data)
        return final_out, data
        # f = open('test.txt', 'w')
        # f.write(final_out)
                # sys.exit()

    def extract_text(self, element, is_table = False):
        #for ref in element.find_all('sup', {"class" : ['reference', 'noprint', 'Inline-Template']}):
        for ref in element.find_all('sup'):
            ref.decompose()
        for span in element.find_all('span', attrs={'id': lambda x: 'coordinates' == x}):
            span.decompose()
        for br in element.find_all("br"):
            br.replace_with("\n")

        for a in element.findAll('a'):
            if a.has_attr('class') and ('external' in a.get('class') or 'extiw' in a .get('class')):
                a.decompose()
            elif  a.has_attr('href'):
                if'footnote' in a['href'].lower() or 'file' in a['href'].lower() or 'cite' in a['href'].lower():# or 'http://185.232.71.186/' not in a['href']:
                    a.decompose()
                else:
                    a.replace_with('[[' + a['href'].split('/')[-1] + '|' +  a.get_text() + "]]")
        if is_table:
            for li in element.find_all(["li", "ul", "ol", "dl"]):
                li.decompose()
        else:
            for li in element.find_all(["li", "ul", "ol", "dl", "div"]):
                li.decompose()
        text = element.get_text().strip()
        text = text.replace('Category:', ':Category:')
        text = re.sub("\[[0-9]+\]", "", text)
        text = re.sub(r'\[\[http(.+?)\|(.+?)\]\]', r'\2', text)
        text = re.sub(r'\[\[(.+?)\|http(.+?)\]\]', r'\1', text)
        text = text.replace('[[[', '[[')
        text = text.replace(']]]', ']]')
        text = text.replace('[[|', '[[')
        text = text.replace('|]]', ']]')
        text = text.replace('•', ' ')

        # text = re.sub(r'\[\[(.+?).php(.+?)\|(.+?)\]\]', r'\2', text)
        # text =re.sub(r'\w*\?pagename=\w*', '', text)
        # text =re.sub(r'\w*\&params=\w*', '', text)
        # text = text.replace(' , ', ', ')
        return text


    def convert_table_to_wikidata(self, table, caption, data, is_infobox = False):
        content = []
        if is_infobox:
            content.append('<span style="visibility: hidden;font-size:1px">{}_table_infobox_{}</span>'.format(self.title, self.table_id))
            data['table_{}'.format(self.table_id)] = {'table': [], 'type': 'infobox'}
            content.append('{|class="wikitable" style="border: none; width: 25%; background: none; float: right;')
        else:
            content.append('<span style="visibility: hidden;font-size:1px">{}_table_general_{}</span>'.format(self.title, self.table_id))
            data['table_{}'.format(self.table_id)] = {'table': [], 'type': 'general'}
            content.append('{|class="wikitable"')
        if caption:
            content.append('|+ ' + caption + '<span style="visibility: hidden;font-size:1px">' + self.title + '_table_caption_' + str(self.table_id) + '</span>')
            data['table_{}'.format(self.table_id)]['caption'] = caption
        data['order'].append('table_{}'.format(self.table_id))
        current_id = self.table_id
        self.table_id +=1

        for i, row in enumerate(table):
            curr_row = []
            curr_row_wiki = []
            for j,entry in enumerate(row):
                if entry == None:
                    continue
                values = entry.split('[SEP]')
                if values[3] == 'th':
                    #content.append('!rowspan="' + values[2] + '", colspan="' + values[1] + '" |' + values[0] + '<span style="visibility: hidden;font-size:1px">' + self.title + '_header_cell_' + str(current_id) + '_' + str(i) + '_' + str(j) + '</span>')
                    curr_row.append({'value': values[0], 'is_header': True, 'column_span':values[1], 'row_span': values[2]})
                    curr_row_wiki.append('!rowspan="' + values[2] + '", colspan="' + values[1] + '" |' + values[0] + '<span style="visibility: hidden;font-size:1px">' + self.title + '_header_cell_' + str(current_id) + '_' + str(i) + '_' + str(j) + '</span>')
                else:
                    #content.append('|rowspan="' + values[2] + '", colspan="' + values[1] + '" |' + values[0] + '<span style="visibility: hidden;font-size:1px">' + self.title + '_cell_' + str(current_id) + '_' + str(i) + '_' + str(j) + '</span>')
                    curr_row_wiki.append('|rowspan="' + values[2] + '", colspan="' + values[1] + '" |' + values[0] + '<span style="visibility: hidden;font-size:1px">' + self.title + '_cell_' + str(current_id) + '_' + str(i) + '_' + str(j) + '</span>')
                    curr_row.append({'value': values[0], 'is_header': False, 'column_span':values[1], 'row_span': values[2]})
            if len(curr_row) == 1 and curr_row[0]['value'] == '':
                continue
            else:
                content += curr_row_wiki
                content.append('|-')
                data['table_{}'.format(current_id)]['table'].append(curr_row)
        content.append('|}')
        # print('\n'.join(content))
        return content

    def parse_table(self, table, is_infobox = False):
        output = []
        def insert_cell(i, j, val, height, width, type, class_val):
            while i >= len(output):
                output.append([])
            while j >= len(output[i]):
                output[i].append(None)

            if output[i][j] is None:
                if class_val:
                    output[i][j] = val.strip() + '[SEP]' + str(width) + '[SEP]' + str(height) + '[SEP]' + type + '[SEP]' + '[LIST_SEP]'.join(class_val)
                else:
                    output[i][j] = val.strip() + '[SEP]' + str(width) + '[SEP]' + str(height) + '[SEP]' + type
        def insert(i, j, height, width, val, type, class_val):
        # pdb.set_trace()
            for ii in range(i, i +1 ):
                for jj in range(j, j + 1):
                    insert_cell(ii, jj, val, height, width, type, class_val)

        def insert_correct_table(i, j, height, width, val):
        # pdb.set_trace()
            for ii in range(i, i+height):
                for jj in range(j, j+width):
                    insert_cell(ii, jj, val, height, width)

        def check_cell_validity(i, j):
            if i >= len(output):
                return True
            if j >= len(output[i]):
                return True
            if output[i][j] is None:
                return True
            return False
        row_ind = 0
        col_ind = 0
        column_size = None

        row_size = len(list(table.find_all('tr')))
        row_mem = [0] * row_size
        # print('meep')
        for i, row in enumerate(table.find_all('tr')):
            smallest_row_span = 1

            if is_infobox and len(list(row.findAll(['td', 'th']))) == 1 and row.find('td'):
                continue

            # if is_infobox and len(list(row.children)) == 1 and list(row.children)[0].name == 'td':
            #     continue

            for cell in row.children:

                if cell.name in ('td', 'th'):
                    row_span = int(cell.get('rowspan').replace('!', '')) if cell.get('rowspan') else 1

                    if row_span > row_size - i:
                        row_span = row_size - i

                    for j in range(i + 1, i + row_span):
                        row_mem[j] += 1
                    # try updating smallest_row_span
                    smallest_row_span = min(smallest_row_span, row_span)
                    # check multiple columns
                    col_span = int(cell.get('colspan').replace('!', '')) if cell.get('colspan') else 1
                    # find the right index
                    while True:
                        if check_cell_validity(row_ind, col_ind):
                            break
                        col_ind += 1
                    try:
                        insert(row_ind, col_ind, row_span, col_span, self._transformer(self.extract_text(cell, is_table = True)), cell.name, cell.get('class'))
                    except UnicodeEncodeError:
                        raise Exception( 'Failed to decode text; you might want to specify kwargs transformer=unicode' )
                        #traceback.print_exc()
                    # update col_ind
                    col_ind += col_span
            # update row_ind
            # print(col_ind)
            # print('adjusted', col_ind + row_mem[i])
            if column_size == None:
                column_size = col_ind
            elif column_size != col_ind + row_mem[i] and not (column_size < col_ind + row_mem[i] and len(list(row.children)) == 1):
                err  = 'Column sizes do not match across rows. Skipping table in article {} ...'.format(self.title)
                raise RuntimeError(err)

            row_ind += smallest_row_span
            col_ind = 0
        return output

#url = 'https://en.wikipedia.org/wiki/Glossary_of_British_terms_not_widely_used_in_the_United_States'
# extractor.parse_article(url, 'Anarchism')
# url = 'https://en.wikipedia.org/wiki/Afroasiatic_languages'
#
#

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class Counter(object):
    def __init__(self):
        self.val = multiprocessing.Value('i', 2) #Sets iniital id to 2

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    @property
    def value(self):
        return self.val.value



#cut everything before  14674000
if __name__ == '__main__':

    mode = sys.argv[1]


    if len(sys.argv) > 2:
        directory = sys.argv[2]



    if len(sys.argv) > 3:
        out_path = sys.argv[3]
        if not os.path.exists(os.path.join(out_path)):
            os.makedirs(os.path.join(out_path))


    if mode == 'clean':
        from os import walk

        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if  file.endswith(".gz"):
                    file_paths.append(os.path.join(root,file))


        acc_name = []
        for file in file_paths:
            file_name = file.split('/')[-1].split('.')[0]
            if file_name.endswith('44') and int(file_name) < 14670000:
                os.remove(file)

    elif mode == 'test':

        count_per_file = 0
        current_count = 0
        data_processed = {}
        extractor = Extractor()
        url = 'https://en.wikipedia.org/wiki/Eudonia_bisinualis'#Publius_Cornelius_Rutilus_Cossus'#$Swift_Justice'#A_Young_Doctor%27s_Notebook_(TV_series)'#'https://en.wikipedia.org/wiki/Talladega_County,_Alabama'
        title = ''
        doc = urlopen(url)
        content, data = extractor.parse_article(doc, title)
        data_processed[title] = data
        f = open('processed_test.txt', 'w')
        f.write(content)
        with open('data_processed.json', 'w') as outfile:
            json.dump(data, outfile)


    elif mode == 'process':


        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if  file.endswith(".gz"):
                    file_paths.append(os.path.join(root,file))


        # file_path_chunks = list(chunks(file_paths, 1500))
        #
        # print(file_path_chunks)



        #IMPORTANT INCREMENT HERE!!!!!
        #DONE: 0 1 2

        current_chunk =  3


        # out_path_original = out_path
        # # for chunk in file_path_chunks:
        # out_path = out_path_original + '/part{}'.format(str(current_chunk))

        if os.path.isfile(os.path.join(out_path, 'wikipedia_processed.xml')):
            os.remove(os.path.join(out_path, 'wikipedia_processed.xml'))

        # if current_chunk > 0:
        #     titles = []
        #     for ch in range(current_chunk):
        #         content_title = open(os.path.join(out_path_original, 'part{}'.format(ch), 'titles.txt'), 'r').readlines()
        #         titles += [el.strip() for el in content_title]
        #     print(titles[:1000])
        #     titles = set(titles)
        # else:
        #     titles = []

        if not os.path.exists(os.path.join(out_path, 'wiki-pages')):
            os.makedirs(os.path.join(out_path, 'wiki-pages'))

        if os.path.isfile(os.path.join(out_path, 'data_processing.log')):
            os.remove(os.path.join(out_path, 'data_processing.log'))

        logging.basicConfig(filename=os.path.join(out_path, 'data_processing.log'), filemode = 'a', level=logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s', datefmt = '%m/%d/%Y %I:%M:%S')



        data_all = {}
        # id = 2
        counter = Counter()
        count_per_file = 10000
        current_file = 0
        current_article = 0
        titles = set([])
        titles_file = open(os.path.join(out_path, 'titles.txt'), 'w')
        wikipedia_dump =  open(os.path.join(out_path, 'wikipedia_processed.xml'), 'a')
        now = datetime.now()
        wikipedia_dump.write("""<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">
          <siteinfo>
            <sitename>Wikipedia</sitename>
            <dbname>enwiki</dbname>
            <base>https://en.wikipedia.org/wiki/Main_Page</base>
            <generator>MediaWiki 1.36.0-wmf.18</generator>
            <case>first-letter</case>
            <namespaces>
              <namespace key="0" case="first-letter" />
            </namespaces>
          </siteinfo>""")

        def process_file(member):
            title, content = member
            extractor = Extractor()
            #print(title)
            try:
                processed_content, processed_data = extractor.parse_article(content, title)
                processed_content =  saxutils.escape(processed_content)
                # titles_file.write('{}\n'.format(title))
                # contributor = 'Credits to the contents of this page go to the authors of the corresponding Wikipedia page: en.wikipedia.org/wiki/{}.'.format(saxutils.escape(title))
                wikipedia_string = "<page>\n<title>{}</title>\n<ns>0</ns>\n<id>{}</id>\n<revision>\n<id>{}</id>\n<timestamp>{}</timestamp>\n<model>wikitext</model>\n<format>text/x-wiki</format>\n<text>{}</text>\n</revision>\n</page>\n".format(title, 0, 0, now, processed_content)
                return [wikipedia_string, processed_data, title]
            except Exception as inst:
                logging.info('Error while processing {}'.format(title))
                logging.info(inst)
                #traceback.print_exc()
                return None


        for lob, file in enumerate(tqdm(file_paths)):
            print('Start extraction...')
            extracted_tars = []
            with tarfile.open(file, "r:gz") as tar:
            # tar = tarfile.open(file, "r:gz") #13881844.tar.gz  13882000.tar.gz
                logging.info('Reached tar {}'.format(file))
                try:
                    members = tar.getmembers()
                    for member in members:
                        f = tar.extractfile(member)
                        title = unquote(member.name).split('/')[-1].split('.html')[0].replace('_', ' ')
                        title = saxutils.escape(title)
                        tar_name = int(file.split('/')[-1].split('.')[0])
                        if f is not None and ((tar_name > 14662000 and tar_name < 14687844) or title not in titles):
                        # if f is not None and title not in titles:
                             content = f.read()
                             extracted_tars.append((title,content))
                             titles.add(title)
                except Exception as inst:
                    logging.info('Error while processing compressed file {}'.format(file))
                    logging.info(inst)
                    traceback.print_exc()
                    continue

            print('Extraction finished. Start processing...')
            with Pool(4) as p:
                for num, results in enumerate(p.imap(process_file, extracted_tars)):
                    current_article +=1
                    if current_article % 1000 == 0:
                        logging.info('Procssed {} files'.format(str(current_article)))
                    if results != None:
                        wikipedia_string, processed_data, title = results
                    else:
                        continue
                    # (filename, count) tuples from worker
                    wikipedia_dump.write(wikipedia_string)
                    titles_file.write('{}\n'.format(title))
                    if (current_article + 1) % count_per_file == 0:
                        print('Writing JSON...')
                        logging.info('Writing into JSON {}'.format(str(current_file)))
                        with open(os.path.join(out_path, 'wiki-pages', 'wiki_{0:0=3d}.json'.format(current_file)), 'w') as outfile:
                            json.dump(data_all, outfile)
                        current_file +=1
                        data_all = {}
                    else:
                        data_all[title] = processed_data
            print('Processing finished.')

        with open(os.path.join(out_path, 'wiki-pages', 'wiki_{0:0=3d}.json'.format(current_file)), 'w') as outfile:
            json.dump(data_all, outfile)
        wikipedia_dump.write('</mediawiki>')
