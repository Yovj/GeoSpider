# -*- encoding: utf-8 -*-
import urllib2
import re


class cx_extractor_Python:
    """cx_extractor implemented in Python"""

    __text = []
    __threshold = 86
    __indexDistribution = []
    __blocksWidth = 3

    def getText(self, content):
        lines = content.split('\n')
        #self.__indexDistribution.clear()
        for i in range(0, len(lines) - self.__blocksWidth):
            wordsNum = 0
            for j in range(i, i + self.__blocksWidth):
                lines[j] = lines[j].replace("\\s", "")
                wordsNum += len(lines[j])
            self.__indexDistribution.append(wordsNum)
        start = -1
        end = -1
        boolstart = False
        boolend = False
        for i in range(len(self.__indexDistribution)-1):
            if(self.__indexDistribution[i] > self.__threshold and (not boolstart)):
                if (self.__indexDistribution[i + 1] != 0 or self.__indexDistribution[i + 2] != 0 or self.__indexDistribution[i + 3] != 0):
                    boolstart = True
                    start = i
                    continue
            if (boolstart):
                if (self.__indexDistribution[i] == 0 or self.__indexDistribution[i + 1] == 0):
                    end = i
                    boolend = True
            tmp = []
            if(boolend):
                for ii in range(start, end+1):
                    if(len(lines[ii]) < 5):
                        continue
                    tmp.append(lines[ii]+"\n")
                str = "".join(list(tmp))
                if (u"Copyright" in str or u"版权所有" in str):
                    continue
                self.__text.append(str)
                boolstart = boolend = False
        result = "".join(list(self.__text))
        return result

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES={'nbsp': ' ', '160': ' ',
                    'lt': '<', '60': '<',
                    'gt': '>', '62': '>',
                    'amp': '&', '38': '&',
                    'quot':'"','34':'"',}
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()
            key = sz.group('name')
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                #以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def getHtml(self, url):
        page = urllib2.urlopen(url)
        html = page.read()
        return html.decode("utf-8")

    def readHtml(self, path):
        page = open(path, encoding='GB18030')
        lines = page.readlines()
        s = ''
        for line in lines:
            s += line
        page.close()
        return s

    def filter_tags(self, htmlstr):
        re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
        re_script = re.compile('<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
        re_style = re.compile('<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
        re_textarea = re.compile('<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+.*?>', re.DOTALL)
        re_comment = re.compile('<!--.*?-->', re.DOTALL)
        re_space = re.compile(' +')
        s = re_cdata.sub('', htmlstr)
        s = re_script.sub('', s)
        s = re_style.sub('', s)
        s = re_textarea.sub('', s)
        s = re_br.sub('', s)
        s = re_h.sub('', s)
        s = re_comment.sub('', s)
        s = re.sub('\\t', '', s)
        # s = re.sub(' ', '', s)
        s = re_space.sub(' ', s)
        s = self.replaceCharEntity(s)
        return s

cx = cx_extractor_Python()
html = cx.getHtml('http://blog.sina.com.cn/s/blog_4969c6830102wx8j.html?tj=1')
content = cx.filter_tags(html)
s = cx.getText(content)
print s