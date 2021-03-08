import sys
from bs4 import BeautifulSoup
from xml.sax import saxutils
import re

if __name__ == '__main__':

    mode = sys.argv[1]


    if mode == 'escape_title':

        path = sys.argv[2]

        out_path = sys.argv[3]

        in_file = open(path, 'r')

        def match_function(match):
            group = match.group(1)
            return '<title>' + group.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') + '</title>'
        content = in_file.read()
        content = re.sub(r'<title>(.+)</title>', match_function, content)
        
        out_file = open(out_path, 'w')

        out_file.write(content)

        # soup = BeautifulSoup(in_file.read(), features="xml")
        #
        # # print(soup)
        #
        # out_file = open(out_path, 'w')
        #
        # content = soup.findAll('title')
        # for i, element in enumerate(content):
        #     print(element.name)
        #     if element.name == 'title':
        #         print(element)
        #         element.stringsax = saxutils.escape(element.text)
        #         print(element)



        # out_file.write(content)
