## scrape.py 
## has hardcode url endpoint 

from bs4 import BeautifulSoup
import requests

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
    t = a[p+1:-1]
    s = Speech()
    c = SpeechContent()
    c.type = "Speech"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:-1]
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
    c.text = f[p+1:-1]
    c.name = f[0:p]
    return c
    
def parseContinueSpeech(tag):
    c = SpeechContent()
    c.type = "ContinueSpeech"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:-1]
    c.name = f[0:p]
    return c

def parseIntervention(tag):
    c = SpeechContent()
    c.type = "Intervention"
    f = flatten(tag)
    p = f.index(':')
    c.text = f[p+1:-1]
    c.name = f[0:p]
    return c

## main stuff here

bills = []
r = requests.get("https://www.parliament.nz/en/pb/hansard-debates/rhr/combined/HansD_20170726_20170726")

data = r.text
soup = BeautifulSoup(data, "html.parser")

count = 1
for body in soup.find_all('body'):
    n = body.find_all('body')
    for b2 in n:
        p = b2.find_all('p')
        currentBill = None
        currentSpeech = None
        for para in p:
            c = para['class'][0]
            #print(c)
            if c == "BillDebate":
                bill = BillDebate()
                bill.title = flatten(para)
                bills.append(bill)
            if c == "SubDebate":
                if len(bills) > 0:
                    currentBill = bills[-1]
                    currentBill.subTitle = flatten(para)
            if c == "Speech":
                if currentBill != None:
                    currentSpeech = parseSpeech(para)
                    currentBill.speeches.append(currentSpeech)
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
print("<Bills>")
for b in bills:
    xml = b.asXML().encode('utf-8')
    print(xml )

print('</Bills>')