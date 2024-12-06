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

here = os.path.realpath('./')
dir = os.fsencode(here)
for f in os.listdir(dir):
  filepath = os.fsdecode(f)
  if(filepath.endswith(".bpmn")):
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
                    documentation = docelmts[i].contents[0]


                documentationDE = getproperty(elmt, 'elementDocumentationDE')
                docref = getproperty(elmt, 'referencedDocument')
                docrefDE = getproperty(elmt, 'referencedDocumentDE')
                name = elmt['name'].encode('utf-8')

                writer.writerow([elmt.get('id'),name.decode('utf-8'), nameDE, documentation, documentationDE, docref, docrefDE])



# with open('csvout.csv', 'w') as csvfile: #filepath+".csv", "w") as csvfile:
#   csvfile.write(u'\uFEFF')
#   csvfile.write(csv)




#input("enter to close")




