import os
from bs4 import BeautifulSoup, NavigableString
import csv
from pathlib import Path


here = os.path.realpath('./')
bpmn = ""

def getNamespace():
  bpmndef = bpmn.find("bpmn:definitions")
  semanticdef = bpmn.find("semantic:definitions")
  bpmn2def = bpmn.find("bpmn2:definitions")

  if bpmndef is not None:
    #Use the bpmn namespace
    return "bpmn"
  elif semanticdef is not None:
    #use the semantic namespace
    return "semantic"
  elif bpmn2def is not None:
    return "bpmn2"
  else:
    print("ERROR: Unknown namespace")
    return "bpmn"

def addProperty(elmt, attr, value):
  if value == "":
    return
  #This does not read NC or other extension elements; modelervs only
  prop = elmt.find('modelervs:property', attrs={"name":attr})

  if prop is not None:
    prop['value'] = value
  else:
    prop = bpmn.new_tag("modelervs:property", attrs={"name": attr, "value": value})

    extParent = elmt.find(['bpmn:extensionElements','bpmn2:extensionElements', 'semantic:extensionElements'], recursive=False)

    if extParent is None: 
      extParent = bpmn.new_tag(getNamespace()+":extensionElements")
      elmt.insert(0,extParent)
    extParent.append(prop)
  return


dir = os.fsencode(here)
for f in os.listdir(dir):
  filepath = os.fsdecode(f)
  if filepath.endswith(".bpmn"):
    print(filepath)

    with open(Path(filepath).stem+".csv", 'r', newline='') as csvfile:
      reader = csv.reader(csvfile)
      next(reader)
      
      with open(filepath, 'r', encoding='utf-8') as bf:
        bpmn = BeautifulSoup(bf, features="xml")

        defn = bpmn.find(["bpmn:definitions","semantic:definitions", "bpmn2:definitions"])

        if bpmn.get("xlmns:modelervs") is None:
          defn['xmlns:modelervs'] = "http://"
        # xmlns:modelervs="http://"

        for line in reader:
          elmt = bpmn.find(id=line[0])
          if elmt and elmt.get('name'):
            elmt['name'] = line[1] #name
            #nameDE
            addProperty(elmt, "nameDE", line[ 2])
            # elmt.name = line[3] #documentation
            if line[3] != "":
              docelem = elmt.find(["bpmn:documentation", "semantic:documentation", "bpmn2:documentation"])
              if docelem is None:
                docelem = bpmn.new_tag(getNamespace() + ":documentation")
                elmt.insert(0,docelem)
              docelem.string = line[3]

            addProperty(elmt, "elementDocumentationDE", line[4])

            addProperty(elmt, "referencedDocument", line[5])

            addProperty(elmt, "referencedDocumentDE", line[6])
          else:
            print(f"Warning: this element is invalid: {line[0]}")

      print("Successfully generated a diagram, char length: "+str(len(str(bpmn))))

      if not(os.path.exists("output")):
        os.makedirs("output")
        print("Just made a directory : "+str(os.path.exists("output")))
      if(not(os.path.exists('output/translated_'+filepath))):
        print("document doesnt exist yet. Trying to create")
        try:
          open('output/translated_'+filepath, 'a').close()
          print('created!')
        except Exception as e:
          print(e)
          open('test-main-dir.txt','a').close()
          open('output/test-sub-dir.txt','a' ).close()
      with open('output/translated_'+filepath, 'a+', encoding = 'utf-8') as translated:
        translated.write(str(bpmn))
