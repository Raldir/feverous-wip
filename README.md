# Multimodal-FEVER

## Installation of Mediawiki

1. Follow the installation guide of Mediaiwki on: https://www.mediawiki.org/wiki/Manual:Running_MediaWiki_on_Debian_or_Ubuntu
2. Please also run the step for `Configure PHP` and set the limit to maximum file file size to a reasonably high size (>20MB).
3. I used Apache2 to put Mediawiki online on my domain but anything should be fine (Not sure what you use internally).
3. When the installation has finished, and you start configuring MediaWiki by going to the webpage, please configure it similarly to how I did it, if possible. First check that the environmental checks are fine: ![GitHub Logo](Images/wikimedia_installation01.png)
For the specific configuration of Mediawiki please look at `Wikimedia-setupLocalSettings.php`. After the configuration has been finished, you can directly compare the LocalSettings.php file generated for the new Mediawiki page with the file in this repository.  
4. Navigate to Common.css (e.g. http://fever.raly.me/index.php/MediaWiki:Common.css) and paste the code of `Wikimedia-setup/Common.css` into it. This will hide all parts of Wikimedia we do not want to show the user. All functionality will remain active, so to login as an admin the common GET requests can still be used (e.g. http://fever.raly.me/index.php?title=Special:UserLogin when logging in).
5. Setup of the favicon.ico: Simply put the file `Images/favicon.ico` into the root level of the Mediawiki installation.

## Uploading Wikipedia pages to Mediawiki

1. The processed Wikipedia dump can be found here: `Wikipedia-articles/wiki_small_processed.xml` (This is a small version. The full Wikipedia dump is still being generated). For manually processing a Wikipedia dump see (#Processing-Wikipedia-dump).
2. Upload the dump to the Mediawiki server following https://www.mediawiki.org/wiki/Manual:Importing_XML_dumps, I have only used `importDump.php`. For big datasets it is recommended to use `mwdumper`, however, it apparently does not work for Mediawiki versions beyond 1.31. If the `importDump.php`is too slow, a mediawiki version of 1.30 can be installed, then the mwdumper can be run and finally the mediawiki installation can be upgraded to 1.35.

## Set up the annotation server
To setup the annotation server itself follow these steps:
0. Put this repository into the root level of the Wikimedia installation.
1. In the folder of this repo `annotation-service/`, create a file `annotation-service/db_params.ini`and specify the `user` and `password` for the existing database. If the servername is not the localhost, it has to be adjusted in ALL files manually (or tell me that I should make a parameter of it like user and password to spare you some annoying work).
2. In `annotation-service/`run `php setup_db.php` to set up the annotation database and to create some dummy entries. All tables are created in the Database `FeverAnnotationsDB`, . There should be four tables now with two users: `ClaimAnnotationData`, `Claims`, `Evidence`, and `Annotators`.   
3. For the evidence annotations, I am doing a redirect to the search page after each annotation. Since the redirect is hard-coded I would need the URL of the Mediawiki server so I can adjust it.


## Processing Wikipedia dump
To manually process the Wikipedia dump do:

1. Install Wikiextractor: `python3 -m pip install wikiextractor` (does not work properly with python3.8 so use python3.7). Modify the package contents (the github repo is corrupt so cannot be installed and modified from source) in /home/[USER]/.local/lib/python3.7/site-packages/wikiextractor/WikiExtractor.py and replace the source code with the one in `Wikipedia-articles/Wikiextractor.py`.
2. Download and put the current Wikipedia dump into a folder `Wikipedia-articles/wiki_full/`.
3. Run 
```
python3.7 -m wikiextractor.WikiExtractor wiki_full/wiki-full.xml -l --keep_tables --html --lists -o wiki_full/wikiextractor -it abbr,b,big
```
4. Download StanfordCoreNLP and install stanza: `python3 -m pip install stanza` and set the environment variable: 
CORENLP_HOME=[PATH_TO_FOLDER]/stanford-corenlp-4.1.0
5. Run
```
python3.8 process_document.py wiki-full/wikiextractor
```

6. Run 
```
 python3 inject_xml.py wiki-full/processed/ wiki_full/wiki-full.xml wiki_full_processed.xml
```
