
Not recommended for general use (very buggy). Extracts BPMN data into a CSV file for easy translation, and generates a new BPMN file with the translations integrated.
Installation:
  Installer python: https://www.howtogeek.com/197947/how-to-install-python-on-windows/
  Passer cette commande sur le command line: (ceci installe des librairies python qui sont utilisées dans l'outil)
    pip install bs4 lxml

Utilisation:

  1. Mettre tous les diagrammes BPMN dans le même fichier que "MakeCSV1.py" et "MakeBPMN2.py".
  2. Double-clicker sur "MakeCSV1.py". Ceci génère un fichier CSV pour chaque diagramme.
  3. Remplir les fichiers CSV avec les traductions voulues.  Attention, les champs existants (Name et Documentation) seront changés aussi. Veillez à utiliser l'encoding "UTF-8", sinon les caractères à accent risquent de sortir faux.
  4. Quand les CSV sont complets, double-clicker sur "MakeBPMN2.py". Ceci génère les nouveaux diagrammes BPMN traduits.
  5. Retrouver les nouveaux diagrammes BPMN dans le fichier "output".

Et dites-moi si quelque chose ne convient pas! kirsten.hauck@processcentric.ch


-----
Installation:
  Install python: https://www.howtogeek.com/197947/how-to-install-python-on-windows/
  Run this command on command line/terminal: (This installs some packages that the script uses)
    pip install bs4 lxml

Using the script:
  1. Put all the BPMN diagrams in the same folder as this program.
  2. Run "CSVMaker.py". You can either double-click on it, or go to the folder in your command line and run "python MakeCSV1.py".
  3. You will now have CSV documents for each bpmn diagram. Edit those (usually with Excel or something similar) to include your translations. If your editor asks you what encoding to use, choose "UTF-8".  WARNING: if you edit the existing fields, your modifications will also end up in the final diagram.
  4. When you have finished translating, run "BPMNDiagramMaker.py", again by double-clicking on it or running "python MakeBPMN2.py".
  5. Your new diagrams should now be in the "output" folder.

If there's trouble, contact me at: kirsten.hauck@processcentric.ch
