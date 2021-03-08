import sys
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from bs4 import BeautifulSoup
import os
import tarfile
import re
import nltk

def extract_text(element):
    #for ref in element.find_all('sup', {"class" : ['reference', 'noprint', 'Inline-Template']}):
    for ref in element.find_all('sup'):
        ref.decompose()
    for br in element.find_all("br"):
        br.replace_with("\n")

    for a in element.findAll('a'):
        if a.has_attr('class') and 'external' in a.get('class'):
            a.decompose()
        elif  a.has_attr('href'):
            if'footnote' in a['href'].lower() or 'file' in a['href'].lower() or 'cite' in a['href'].lower():# or 'http://185.232.71.186/' not in a['href']:
                a.decompose()
            else:
                a.replace_with('[[' + a['href'].split('/')[-1] + '|' +  a.get_text() + "]]")
    for li in element.find_all("[li, ul, ol, dl, div]"):
        li.decompose()
    text = element.get_text().strip()
    text = text.replace('Category:', ':Category:')
    text = re.sub("\[[0-9]+\]", "", text)
    text = re.sub(r'\[\[http(.+?)\|(.+?)\]\]', r'\2', text)
    text = re.sub(r'\[\[(.+?)\|http(.+?)\]\]', r'\1', text)
    text = text.replace('[[|', '[[')
    text = text.replace('|]]', ']]')
    text = text.replace('•', ' ')

    return text


def get_sentences(file_paths):
    sent_num = 50000 #5000
    curr_sent = 0
    sentences = []

    print("Loading sentences...")
    for file in file_paths:
        tar = tarfile.open(file, "r:gz") #13881844.tar.gz  13882000.tar.gz
        try:
            members = tar.getmembers()
            for member in members:
                f = tar.extractfile(member)
                if f == None:
                    continue
                content = f.read()
                soup = BeautifulSoup(content, 'lxml')
                body = soup.find("div", {"class": "mw-parser-output"})
                content = body.findAll('p', recursive=False)
                for i, element in enumerate(content):
                    sentences.append(extract_text(element).replace('\n', ' '))
                    curr_sent +=1
                    if curr_sent> sent_num:
                        return sentences
        except Exception as inst:
            print(inst)
    return sentences

if __name__ == '__main__':

    directory = sys.argv[1]
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if  file.endswith(".gz"):
                file_paths.append(os.path.join(root,file))
    text = ' '.join(get_sentences(file_paths))


    print('Training Splitter..')

    trainer = PunktTrainer()
    trainer.train(text)
    sent_tokenizer = PunktSentenceTokenizer(trainer.get_params())


    print(sent_tokenizer._params.abbrev_types)
    print(sent_tokenizer._params.collocations)
    print(sent_tokenizer._params.sent_starters)
    #
    # extra_abbreviations = list(set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc', 'i.e', 'e.g', 'eg', 'ie', 'c.f', 'b.c.e', 'pg', 'm.a', 'd.c', 'gen', 'cb', 'h.g', 'å', 'ms', 'col', 'mr', 'bros', 'lbf', 'mc', 'jr', 'rep', 'gcs', 'µci', 'op', 'vol', 'pot', 'mya', 'w.e.b', 'c.e', 'est', 'l.c', 'maj', 'o.b', 'e.t.a', 'sp', 'bi', 'a.m.i', 'r', 'pp', 'verified', 'pl', 'g.a.t.c', 'o.k', 'igo', '|mr', 'u.n', 'zrn', 'n.v', 'w', 'dr', 'inc', 'e.g', 'sr', 'a23', 'a.d', 'f.o', '−δh', 'ca', 'w.c', 'f.c', 'sen', 'u.s.n', 'rt', 'fl', 'e.w', 'd.a.b.t', 'b.c', 'msc', 'mrs', 'u.s', 'u.k', 's.p.a', 'a.m', 'u.s', 'o.m', 'c', 'corp', 'n.o.i.f', 'spp', 'p.m', 'cir', 'rig', 'u.s.c', 'ypb', 's.a', 'b.v', 'i.e', 'etc', 'c.f.r', 'hon', 'a.c', 'hist', 'd.r', 'stb', 'bros', 'i.a.s', 'vid', 'w', 't.n', 'p.r', 'lat', 'katczinsky', 'w.h', 'e.i', 'p.m', 'epist', 'sanh', 'g.f', 'd.sc', 'u.k', 'khm', 'a.i', 'xxxii', 'ān-', 'xli', 'm.e', 'aδ', 't.c.w', 'ypb', 'p.e.i', 'e.n.e', 's.m', 'b.a', '1/b', 'sr', 'low—i.e', 'const', 'd.m', '|st', 'uts', 'o.t.o', 'în', 'f4v', 'b.p', 'h.g.h', 'n.e', 'h.q', '|mr', 'c.j', 'u.s.a', 'en-', 'j.d', 'f.m', 'd.l', 'ros', 'm.i', 'j.p', 'ka3', 'grs', 'c.s.c', 'n.c', 'vol', 'unrest——viz', 'f.c', 'w.c', "'w", 'm.d', 'a.b.c', '|a.g', 'tosef', 'libr', "'u.s", 'k.p', 'w.e.b', 'adv', 'f.j', '|s', 'g.a.t.c', 'c18', 'deut', 'emph', 'h.t', '|ms', 'a.h', 'u.n', 'j.b.a', '97p', 'nov', 'c.8', 'udc', 'o.s', 'r.v', 'p.j.h', 'd.l.r', 'mek', 'yer', 'm.s', 'c.i.l', 'ams', 'c95', 'c.f.r', 'f.k', '5%p.a', 'etc', 's.d', 'haer', 'j.j', 's.e', 'j.e', 'hurr', '01h', 'e.g', 'től', 'd.c', 'e.j', 'yeb', 'n.s', 'iba', 'ð̴/', 'z.e', 'u.s.n', 'mk.i', '+n', 'p.c.l', 'u.s.c', '|g.d', '1039ff', 's.r.l', 'o.b', 'e.t', 'a.a', 'św', 'c.w', '2am', 'ibid', 'j', 's.o.s', 'u.c.l.a', 'cir', 'seq', 'lib', 'i.e', 'kla', 'jud', 'y.u.c.k', 'vln', 'aro', 'p.s', '−δh', 'mds', 'p.a', 'c.e', 'ک', 'g.j', 'b.s', 'viz', 'b.i.d', 'r.h', 'o-h', 'n.y', 'syn', 'd.a', 'ḳ', 't.r.e.e', 'eṯ-', 'un-', 'ibs', 'll.d', 'h.a', 'a.m', '.h', 'h.p', 'it”', 'v.d', '|dr', 'e.k', 'j.c', 'rd', 'x=1', 'n−c', 'j.c.a', 'l.a', 's.a.s', 'r.b', '_made_in_america|o.j', 'j.m', 'q.e', 'j.f', 'a.k.a', 'c&a', 's.j', 'a.u', "'o.k", 'ph.d', 'aftermath—i.e', 'p.l', 'ᾰᾰ', 'c.q', 't.h.c', 'eds', 'c.c', 'l.c', 'hdt', '⟨ḍ⟩', 'r–n.m', 'c.f.w', 'soz', 'r.i', 'b.v', 'd.a.b.t', 'v.c', 'j.s', 'm.m', 'de/', 'vols', 'a.l', '—i.e', 'a.g', 'a23', 'boc', 'jr', 'us—i.e', 'p.g', 'o.j', 'bvt', 'a.m.i', 'm.a', 'v.w', 'skt', 's.l', 'jur', 'n.v', '|e.t', 'o.k', 'e.t.a', 'e.w', 'd.o', 'aug', 'a.d', '3.5%p.a', 'ie', 's.c.r', 'k.r', 'esq', 'mic', 'hon', 'sgt', 'a.e', 'o.m', 'rug', 'cfr', 'ωij', 'h.g', 'k.u.k', 'abbrev', 'e.v', 'p2y', 'pl', 'r.w', 'uwf', 'j.-c', 'n.o.i.f', 'nil', '|u.s', 'e.l', '11%p.a', 'i.q', '|l.a', 'jer', 'lúi', 'd.j', 'µci', 't.g.i', 'j/', 'ŉ', 'fr', 'b.c', 't.j', 'e.r', 'kb6', 'bfs', 'abbrv', 'αr', 'c.m', 'v.b', 's.k', 'g.n', 'd.p', 'col', 'gcs', 'c.y', 'b.i.g', 'maj', 'n.w', 'vz', 'p67', 'w.a.c', 'akon', 'a.f', 'a.j.j', 'dimensions—e.g', 'me’', 'l.p', 'f.sh.f', 'c.t', 'h.r', 'l.o', 'zrn', 's.s', 'abbr', 'a.c', 'e.u', 'r.s', 'kmt', 'qeq', 'g.d', '/ŭ/', 'fl', 'f.o', 'c.u', 'smg', 'l.h', 'eccl', 'sct', 'ℤ', '/k/', 'eua', 'a.s', 'coh', 'iex', 'gk', 'july/aug', 'rep', '—e.g', 'resp', 'n.n', '|c.s', 'd2o', 'c.s', 'sm̥', 'b.c.e', 'property—i.e', 'č', 's.p.a']))
    # sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    # sent_tokenizer._params.abbrev_types.update(extra_abbreviations)



    test = """'Yes!' is a song co-written and recorded by American country music artist Chad Brock. There are several examples for this e.g. how the system should behave in that way. It is clear that Mr. House should not request an audience. Moreovoer, Dr. Einstein tried to talk to Mr. Shalby about several systems he designed."""
    sents = sent_tokenizer.tokenize(test)
    print(sents)
