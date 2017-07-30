## transform Hansard xml format to Akoma Ntoso 


from __future__ import print_function
import sys
import xml.etree.ElementTree as ET

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class MPLookup:
    mps = { }

    def load(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        list = root.findall('mp')
        for mp in list:
            key = mp.find('name').text
            value = mp.find('id').text
            self.mps[key] = value

    def find(self, key):
        value = self.mps[key]
        return value

class Speech:
    text = []
    by = "" 

    def asXML(self):
        id = mpl.find(self.by)
        x = '<speech by="#'+ id +'">\n'
        x = x + '<from>' + self.by + '</from>\n'
        for t in self.text:
            x = x + '<p>' + t + '</p>\n'
        x = x + '</speech>\n'
        return x

class Petition:
    heading = []
    speeches = []

    def asXML(self):
        x = '<petitions>\n'
        for h in self.heading:
            x = x + '<heading>' + h + '</heading>\n'
        for s in self.speeches:
            x = x + s.asXML()
        x = x + '</petitions>\n'
        return x

class Meta:
    references = []

    def asXML(self):
        x = '''<Meta>
      <references source="#source">
        <TLCOrganization id="source" href="/ontology/organization/ca.open.north.inc" showAs="Open North Inc."/>
        <TLCPerson id="bishop-christopher" href="/ontology/person/bishop-christopher" showAs="CHRIS BISHOP (National)"/>
        <TLCPerson id="little-andrew" href="/ontology/person/little-andrewr" showAs="ANDREW LITTLE (Leader of the Opposition)"/>
        <TLCPerson id="tirikatene-rino" href="/ontology/person/tirikatene-rino" showAs="RINO TIRIKATENE (Labour-Te Tai Tonga)"/>
       <TLCPerson id="borrows-chester" href="/ontology/person/borrows-chester" showAs="The CHAIRPERSON (Hon Chester Borrows)"/>
        <TLCPerson id="sepuloni-carmel" href="/ontology/person/sepuloni-carmel" showAs="Carmel Sepuloni"/>
        <TLCPerson id="curran-clare" href="/ontology/person/curran-clare" showAs="Clare Curran"/>
        <TLCPerson id="dyson-ruth" href="/ontology/person/dyson-ruth" showAs="Hon RUTH DYSON (Labour-Port Hills)"/>
        <TLCPerson id="mallard-trevor" href="/ontology/person/mallard-trevor" showAs="The CHAIRPERSON (Hon Trevor Mallard)"/>
        <TLCPerson id="tisch-lindsay" href="/ontology/person/tisch-lindsay" showAs="The CHAIRPERSON (Lindsay Tisch)"/>
        <TLCPerson id="bennett-paula" href="/ontology/person/bennett-paula" showAs="Hon PAULA BENNETT (Minister of State Services)"/>
        <TLCPerson id="speaker-deputy" href="/ontology/person/speaker-deputy" showAs="Mr Deputy Speaker"/>
        <TLCPerson id="prosser-richard" href="/ontology/person/prosser-richard" showAs="RICHARD PROSSER (NZ First)"/>
        <TLCPerson id="english-bill" href="/ontology/person/english-bill" showAs="Rt Hon BILL ENGLISH (Prime Minister)"/>
 
        <TLCPerson id="speaker" href="/ontology/person/ca-ns.speaker" showAs="Speaker {?}"/>
      </references>

</Meta>
'''
        return x

class Preface:
    docTitle = ""
    docNumber = ""
    docDate = ""
    docAuthority = "parliament.nz"
    legislature ="51st Parliament"
    session = "1st Session?"
    link = ""
    
    def asXML(self):
        x = '<Preface>\n'
        x = x + '<docTitle>' + self.docTitle + '</docTitle>\n'
        x = x + '<docDate>' + self.docDate + '</docDate>\n'
        x = x + '<docAuthority>' + self.docAuthority + '</docAuthority>\n'
        x = x + '<legislature>' + self.legislature + '</legislature>\n'
        
        x = x + '<link rel="alternate" type="text/html" href="' + self.link  + '"/>\n'
        x = x + '</Preface>\n'
        return x

class Question:

    def asXML(self):
        x = '''<questions>
            <question alternativeTo="" as="" by="" class="" endTime="" evolvingId="" id="" lang="" period="" refersTo="" space="" startTime="" status="" style="" title="" to="">{1,1}</question>
            <answer alternativeTo="" as="" by="" class="" endTime="" evolvingId="" id="" lang="" period="" refersTo="" space="" startTime="" status="" style="" title="" to="">{1,1}</answer>
 
        </questions>'''

        return x

class Debate:
    entities = []
    speeches = []
    petitions = []
    preface = Preface()


    def my_func(self):
        if len(self.entities) > 0:
            print('heelo')

    def parseHansard(self, root = None):
        ### preface
        p = root.findall('Preface')[0]
        t = p.find('title').text
        self.preface.docTitle = t
        t = p.find('date').text
        self.preface.docDate = t
        t = p.find('link').text
        self.preface.link = t
        ### speaches
        debates = root.findall('Debates')[0].findall('Debate')
        for d in debates:
            speaches = d.findall('Speeches')[0].findall('Speech')
            for s in speaches:
                currentSpeech = Speech()
                currentSpeech.text = []

                contents = s.findall('SpeechContents')[0].findall('Content')
                for c in contents:
                    type = c.find('type').text
                    text = c.find('text').text
                    name = c.find('name').text
                    if type == 'Interjection' or type == 'ContinueSpeech' or type == 'Intervention':
                        self.speeches.append(currentSpeech)
                        currentSpeech = Speech()
                        currentSpeech.text = []
                    currentSpeech.text.append(text)
                    currentSpeech.by = name
            self.speeches.append(currentSpeech)
        #### Petitions
        bills = root.findall('Bills')[0].findall('BillDebate')
        for bill in bills:
            pet = Petition()
            pet.heading = []
            pet.speeches = []
            h = bill.find('title').text
            pet.heading.append(h)
            h = bill.find('subtitle').text
            pet.heading.append(h)
            speaches = bill.findall('Speeches')[0].findall('Speech')
            for s in speaches:
                currentSpeech = Speech()
                currentSpeech.text = []

                contents = s.findall('SpeechContents')[0].findall('Content')
                for c in contents:
                    type = c.find('type').text
                    text = c.find('text').text
                    name = c.find('name').text
                    if type == 'Interjection' or type == 'ContinueSpeech' or type == 'Intervention':
                        pet.speeches.append(currentSpeech)
                        currentSpeech = Speech()
                        currentSpeech.text = []
                    currentSpeech.text.append(text)
                    currentSpeech.by = name
            pet.speeches.append(currentSpeech)
            self.petitions.append(pet)
            


def makePreface():
    p = Preface()
    return p 

def makeQuestions():
    q = Question()
    return q


def main(filename):
    eprint("[*] transforming "+ filename)
    tree = ET.parse(filename)
    root = tree.getroot()

    global mpl
    mpl = MPLookup()
    mpl.load('mps.xml')
  
    debate = Debate()
    debate.parseHansard(root)


    header = '''<?xml version="1.0"?>
<akomaNtoso>
  <debate name="hansard">
'''
    print(header) 
    # meta
    m = Meta()
    print(m.asXML().encode('UTF-8'))
    # preface
    p = debate.preface
    print(p.asXML().encode('UTF-8'))
    # debate body
    print('<DebateBody>')
    # questions
    q = makeQuestions()
    print(q.asXML().encode('UTF-8'))
    # speeches
    
    for s in debate.speeches:
        print(s.asXML().encode('UTF-8'))

    # petitions

    for x in debate.petitions:
        print(x.asXML().encode('UTF-8'))

    print('</DebateBody>')
    footer = '''
    
  </debate>
</akomaNtoso>
'''
    print(footer)



if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        main(filename)
    else:
        eprint('[*] usage: python transform.py "FILE"')
        eprint('[*]   e.g: python transform.py 20170726.xml')
