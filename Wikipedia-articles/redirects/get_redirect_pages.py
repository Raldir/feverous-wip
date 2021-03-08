import sys
import os
from lxml import etree
from lxml.etree import Element
import re
import shelve



def inject_wikipedia_xml(xml_directory):

    #xml_directory = 'example_articles02/Wikipedia-20201026011851.xml'
    xml_directory = xml_directory#'wiki_s/wiki-small.xml'
    context = etree.iterparse(xml_directory, events=('start',))

    f_redirects = open('redirects.txt', 'w')
    f_redirects.write('{}\t{}\n'.format('origin', 'redirect-destination'))
    with open('redirects.xml', 'wb') as f:
        f.write(str.encode('<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">\n'))
        origin = None
        dest = None
        page_start = False
        curr_page = False
        for action, elem in context:
            #print(elem.tag)
            if 'siteinfo' in elem.tag:
                f.write(etree.tostring(elem, encoding='UTF-8'))
            if 'title' in elem.tag:
                origin = elem.text
            elif 'redirect' in elem.tag:
                dest = elem.get('title')
                # f.write(etree.tostring(elem.getparent(), encoding='UTF-8'))
                # elem.getparent().clear()
            elif 'revision' in elem.tag:
                items = elem
            elif 'text' in elem.tag and dest != None:
                item = Element('text')
                item.text = '#REDIRECT [[{}]]'.format(dest)
                items.replace(elem, item)
                f.write(etree.tostring(items.getparent(), encoding='UTF-8',  pretty_print=True))
                f_redirects.write('{}\t{}\n'.format(origin, dest))
                items.getparent().clear()
                origin = None
                dest = None
            elif 'page' in elem.tag:
                if curr_page:
                    curr_page.clear()
                curr_page = elem
        f.write(str.encode('</mediawiki>'))

if __name__ == '__main__':
    inject_wikipedia_xml(sys.argv[1])

# with open(sys.argv[3], 'wb') as f:
#     f.write(etree.tostring(context.root))
