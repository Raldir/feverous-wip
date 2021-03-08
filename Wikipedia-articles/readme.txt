python3.7 -m wikiextractor.WikiExtractor wiki_small/wiki-small.xml -l --keep_tables --html --lists -o wiki_small/wikiextractor #-it abbr,b,big

NEED To set StanfordCoreNLP at export CORENLP_HOME=/home/raly/bin/stanford-corenlp-4.1.0

python3.8 process_document.py wiki_small/wikiextractor


python3 inject_xml.py wiki-full/processed/ wiki_full/wiki-full.xml wiki_full_processed.xml
