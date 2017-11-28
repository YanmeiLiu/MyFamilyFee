import codecs

import re
from html.parser import HTMLParser


class OptionXml(object):

    def writeXml(self,xmlname,resp):
        tmpxml = codecs.open(xmlname,'w','utf-16')#create a new xml
        tmp1= re.compile(r'\<.*?>')
        tmp2 = tmp1.sub('', resp)
        html_parse = HTMLParser.HTMLParser()
        xmltext = html_parse.unescape(tmp2)

        tmpxml.writelines(xmltext.strip())
        tmpxml.close()



if __name__ == '__main__':
    xmlname = 'ceshi11.xml'
    resp = 'dd'
    ox = OptionXml()
    ox.writeXml(xmlname, resp)

