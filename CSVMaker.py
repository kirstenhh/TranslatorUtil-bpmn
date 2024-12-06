import os
from bs4 import BeautifulSoup, NavigableString
import csv
from pathlib import Path

def getproperty(elmt, attr):
  extelem = elmt.find('modelervs:property', attrs={"name":attr})
  if extelem is not None:
    extelem = extelem.get('value')
  else:
    extelem = ""
  return extelem

def stringchecks(text):
  #This code runs various small text replacements for invalid characters, tabs, Excel quirks etc.
  text = text.rstrip()
  if len(text)<1:
    return text
  print("text: "+text)

  if('\t' in text):
    text = text.replace('\t', ' ')

  text = text.replace('•', '-')
  text = text.replace('', '-')



  if(text[0] == '-'):
    text = "'"+text
    print("hyphens: "+text)
  return text



here = os.path.realpath('./')
dir = os.fsencode(here)
for f in os.listdir(dir):
  filepath = os.fsdecode(f)
  if(filepath.endswith(".bpmn") and not os.path.exists(Path(filepath).stem+'.csv')):

    with open(Path(filepath).stem+'.csv', 'w+', newline='') as csvfile:
      writer = csv.writer(csvfile, dialect='excel')
      writer.writerow(["ID", "Name", "NameDE", "Documentation", "DocumentationDE", "ReferencedDocument", "ReferencedDocumentDE"])
      print(filepath)
      with open(filepath, 'r', encoding='utf-8') as bf:
        bpmn = BeautifulSoup(bf, features ="xml")
        procsonly = bpmn.select('process')
        collaborations = bpmn.select('collaboration')
        processes = procsonly+collaborations
        for proc in processes:
          for elmt in proc.descendants:
            if not isinstance(elmt, NavigableString):

              #If is BPMNElement
              if elmt.get('id') and elmt.get('name'):
                nameDE = getproperty(elmt, 'nameDE')
                docelmts = elmt.select('documentation')
                documentation = ""

                #in almost all documents, it's just docelmts[0].contents. But some diagrams also have an empty docelmt somewhere.
                for i in range(len(docelmts)):
                  if docelmts[i] is not None and len(docelmts[i].contents) >0 and docelmts[i].contents[0] is not None:
                    documentation = stringchecks(docelmts[i].contents[0])


                documentationDE = stringchecks(getproperty(elmt, 'elementDocumentationDE'))
                docref = stringchecks(getproperty(elmt, 'referencedDocument'))
                docrefDE = stringchecks(getproperty(elmt, 'referencedDocumentDE'))
                name = stringchecks(elmt['name']).encode('utf-8')

                writer.writerow([elmt.get('id'),name.decode('utf-8'), nameDE, documentation, documentationDE, docref, docrefDE])



# with open('csvout.csv', 'w') as csvfile: #filepath+".csv", "w") as csvfile:
#   csvfile.write(u'\uFEFF')
#   csvfile.write(csv)




#input("enter to close")




