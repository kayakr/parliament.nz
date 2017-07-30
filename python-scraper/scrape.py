## scrape.py 
## has hardcode url endpoint 

from bs4 import BeautifulSoup
import requests
import sys

class Preface:
    title = ""
    link = ""
    date = ""

    def asXML(self):
        x = '<Preface>\n'
        x = x + '<title>' + self.title + '</title>\n'
        x = x + '<link>' + self.link + '</link>\n'
        x = x + '<date>' + self.date + '</date>\n' 
        x = x + '</Preface>\n'
        return x

class Debate:
    title = ""
    subTitle = ""
    speeches = []

    def asXML(self):
        x = '<Debate>\n'
        x = x + '<title>' + self.title + '</title>\n'
        x = x + '<subtitle>' + self.subTitle + '</subtitle>\n'
        if len(self.speeches) > 0:
            x = x + '<Speeches>\n'
            for s in self.speeches:
                x = x + s.asXML() 
            x = x + '</Speeches>\n'
        x = x + '</Debate>'
        return x

class BillDebate:
    title = ""
    subTitle = ""
    speeches = []

    def asXML(self):
        x = '<BillDebate>\n'
        x = x + '<title>' + self.title + '</title>\n'
        x = x + '<subtitle>' + self.subTitle + '</subtitle>\n'
        if len(self.speeches) > 0:
            x = x + '<Speeches>\n'
            for s in self.speeches:
                x = x + s.asXML() 
            x = x + '</Speeches>\n'
        x = x + '</BillDebate>'
        return x

class Speech:
    by = ""
    time = ""
    content = []
    
    def asXML(self):
        x = '<Speech>\n'
        x = x + '<by>'+ self.by + '</by>\n'
        x = x + '<time>' + self.time + '</time>\n'
        if len(self.content) > 0:
            x = x + '<SpeechContents>\n'
            for sc in self.content:
                x = x + sc.asXML()
            x = x + '</SpeechContents>\n'
            
        x = x + '</Speech>\n'
        return x

class SpeechContent:
    type = ""
    name = ""
    text = ""

    def asXML(self):
        x = '<Content>\n'
        x = x + '<type>' + self.type + '</type>\n'
        x = x + '<name>' + self.name + '</name>\n'
        x = x + '<text>' + self.text + '</text>\n'
        x = x + '</Content>\n'
        return x

def flatten(tag):
    content = ""
    for l in tag:
        if l.string == None:
            content = flatten(l)
        else:
            content = content + l.string
    return content

def parseSpeech(tag):
    a = tag.a['name']
    p = a.index('_')
    t = a[p+1:]
    s = Speech()
    s.content = []
    c = SpeechContent()
    c.type = "Speech"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:]
    c.name = f[0:p]
    s.by = c.name
    s.time = t
    s.content.append(c)
    return s

def parseA(tag):
    sc = SpeechContent()
    sc.text = flatten(tag)
    sc.type = "a"
    return sc

def parseInterjection(tag):
    c = SpeechContent()
    c.type = "Interjection"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:]
    c.name = f[0:p]
    return c
    
def parseContinueSpeech(tag):
    c = SpeechContent()
    c.type = "ContinueSpeech"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:]
    c.name = f[0:p]
    return c

def parseIntervention(tag):
    c = SpeechContent()
    c.type = "Intervention"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:]
    c.name = f[0:p]
    return c


def main(date):
    bills = []
    debates = []
    preface = Preface()

    url = "https://www.parliament.nz/en/pb/hansard-debates/rhr/combined/HansD_" + date + '_' + date
    r = requests.get(url)
    if r.status_code != 200:
        return

    preface.link = url

    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    preface.title = flatten(soup.title)

    count = 1
    for body in soup.find_all('body'):
        n = body.find_all('body')
        for b2 in n:
            p = b2.find_all('p')
            current = None
            currentSpeech = None
            for para in p:
                c = para['class'][0]
                if c == "BeginningOfDay":
                    preface.date = flatten(para)
                if c == "BillDebate":
                    bill = BillDebate()
                    bill.speeches = []
                    bill.title = flatten(para)
                    bills.append(bill)
                    current = bill
                if c == "Debate":
                    debate = Debate()
                    debate.speeches = []
                    debate.title = flatten(para)
                    debates.append(debate)
                    current = debate
                   
                if c == "SubDebate":
                    if current != None:
                        current.subTitle = flatten(para)
                if c == "Speech":
                    if current != None:
                        currentSpeech = parseSpeech(para)
                        current.speeches.append(currentSpeech)
                if c == "a":
                    if currentSpeech != None:
                        s = parseA(para)
                        if s.name == "":
                            s.name = currentSpeech.by
                        currentSpeech.content.append(s)
                if c == "Interjection":
                    if currentSpeech != None:
                        s = parseInterjection(para)
                        currentSpeech.content.append(s)

                if c == "ContinueSpeech":
                    if currentSpeech != None:
                        s = parseContinueSpeech(para)
                        currentSpeech.content.append(s)
                if c == "Intervention":
                    if currentSpeech != None:
                        s = parseIntervention(para)
                        currentSpeech.content.append(s)

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<Hansard>')
    xml = preface.asXML().encode('utf-8')
    print(xml)
    print("<Debates>")
    for b in debates:
        xml = b.asXML().encode('utf-8')
        print(xml )

    print('</Debates>')
    
    print("<Bills>")
    for b in bills:
        xml = b.asXML().encode('utf-8')
        print(xml )

    print('</Bills>')
    print('</Hansard>')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        date = sys.argv[1]
        main(date)
    else:
        print('[*] usage: python scrape.py "DATE"')
        print('[*]   e.g: python scrape.py 20170726')
