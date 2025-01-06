#!/usr/bin/env python3

import os

#in Eclipse F9 drücken, um das Skript laufen zu lassen (ohne Strg!)
#https://stackoverflow.com/questions/7194424/run-external-python-programs-with-eclipse-pydev#7203663

spfad1 = os.path.dirname(__file__) + "/"
spfad2 = spfad1 + "css/"
adateien = ["style.css","style-desktop.css","style-mobile.css"]
#adateien = ["test.css"] #wenn die Tests abgeschlossen sind, kann diese Zeile gelöscht / auskommentiert werden

#Datei einlesen, die die Änderungen enthält
with open(spfad1+"change_color.css", "r") as f: #die Datei könnte man auch in den CSS-Ordner packen, um pfad1 einzusparen
    acssinhalt_neu = f.readlines()
f.close()

#Alle nötigen Daten verarbeiten
"""
- dabei wird darauf gesetzt, dass die einfache Struktur der Datei change_color.css nicht verändert wird,
- das könnte man flexibler mit JSON gestalten
- in einer Entwicklungsumgebung (z.B. Eclipse) können Farbcodes direkt als Farbe (per Hover-Effekt) angesehen...
  ... werden, weshalb die Werte selbst in einer CSS-Datei zu speichern sinnvoll ist 
"""

dictchanges = {datei:{"searchelems":[],"searchattr":[],"newvalues":[],"oldvalues":[]} for datei in adateien}
icurrentline = -2
current_file = ""

for ilinenumber,line in enumerate(acssinhalt_neu):
    line_without_comment = line[2:-3]
    
    if line[2:-3] in adateien:
        current_file = line_without_comment
        
    if "{" in line and current_file != "":
        icurrentline = ilinenumber
        ibracket = line.find("{") #müsste geändert werden, falls nicht in einer Zeile mit CSS-Selektor
        icolon = line.find(":")
        
        #die folgenden vier append Zeilen müssten geändert werden, falls Struktur der Datei geändert wird
        dictchanges[current_file]["searchelems"].append(line[:ibracket])
        dictchanges[current_file]["searchattr"].append(line[ibracket+1:icolon])
        dictchanges[current_file]["newvalues"].append(line[icolon+1:line.find(";")])
        
    if ilinenumber == icurrentline + 1: 
        dictchanges[current_file]["oldvalues"].append(line_without_comment)

###############################################################
#"""

#Dateien ändern
"""
- Hierbei wird auch angenommen, dass an der generellen Struktur der CSS-Dateien nichts verändert wird
"""

bchanged = False

for datei in adateien:
    
    #prüfen, ob in der Datei überhaupt Änderungen vorgenommen werden müssen
    if dictchanges[datei]["newvalues"] != dictchanges[datei]["oldvalues"]:
        
        f = open(spfad2+datei, "r+") #hier könnte man auch with nehmen
        acssinhalt = f.readlines() #Inhalt lesen, dabei wandert der cursor bis zum Ende der Datei
        f.seek(0) #hiermit wird sicher gestellt, dass alles, was hiernach geschrieben wird, ab der 1. Zeile geschrieben wird
        
        belem_found = False #elem ist das gesuchte HTML-Element, also der CSS-Selektor
        
        for ilinenumber,line in enumerate(acssinhalt):
            bchange = False #ob die Zeile verändert wird oder nicht
             
            #falls eine Zeile leer ist oder mit einem Kommentar beginnt, diese überspringen
            if line == "\n" or line[:2].strip() == "/*":
                f.write(line)
                continue
            
            for searchindex, elem in enumerate(dictchanges[datei]["searchelems"]):
                
                #prüfen, ob ein Kommentar nach dem Gesuchten String steht, eoc ist hier Ende des Befehls
                if "/*" in line:
                    eoc = len(line[:line.find("/*")].strip())
                else:
                    eoc = len(line.strip())+2 #müsste geändert werden, falls in einer Zeile mit CSS-Selektor
                    
                #nach CSS-Selektor suchen, falls gefunden, nächste Zeile untersuchen
                if elem == line[:eoc].strip():
                    belem_found = True #müsste geändert werden, falls in einer Zeile mit CSS-Selektor
                    break
                    
                #Ende des Blocks des CSS-Selektors berücksichtigen, falls gefunden, nächste Zeile untersuchen
                if "}" in line:
                    belem_found = False #müsste geändert werden, falls in einer Zeile mit CSS-Selektor
                    break
                
                #prüfen, ob ein Attribut-Wert-Paar in der Zeile ist
                #falls nicht, dann muss nicht nach einem Attribut-Wert-Paar in der Zeile gesucht werden
                if not ":" in line:
                    continue
                
                #Positionen des zu ändernden Wertes herausfinden
                icolon = line.find(":")
                isemicolon = line.find(";")
                if isemicolon < 1:
                    isemicolon = len(line.rstrip())
                    
                #überprüfen, ob das Attribut geändert werden soll
                if line[:icolon].strip() == dictchanges[datei]["searchattr"][searchindex]:
                    aoldvalues = dictchanges[datei]["oldvalues"]
                    
                    #überprüfen, ob der alte Wert in dieser Zeile vorhanden ist
                    if line[icolon+1:isemicolon] in aoldvalues[searchindex]:
                        ssearchvalue_old = aoldvalues[searchindex]
                        snew_value = dictchanges[datei]["newvalues"][searchindex]
                        
                        #falls der alte Wert ungleich dem neuen ist, Änderung einleiten 
                        if ssearchvalue_old != snew_value:
                            bchange = True
                            break
            
            if bchange:
                f.write(line.replace(ssearchvalue_old+";",snew_value+";"))
                bchanged = True
            else:
                f.write(line)
            
        f.close()

###############################################################

#Alte Werte aktualisieren
"""
- Hierbei wird auch angenommen, dass an der generellen Struktur der CSS-Dateien nichts verändert wird
"""

if bchanged:
    with open(spfad1+"change_color.css", "r+") as f:
        acssinhalt_neu = f.readlines()
        f.seek(0)
        
        icurrentline = -2
        current_file = ""
        
        for ilinenumber,line in enumerate(acssinhalt_neu):
            bchange = False
            line_without_comment = line[2:-3]
            
            if line_without_comment in adateien:
                current_file = line_without_comment
                icurrent_attr = -1
                
            if "{" in line and current_file != "": 
                icurrentline = ilinenumber
                icurrent_attr += 1
                
            if ilinenumber == icurrentline + 1: #müsste geändert werden, falls die Struktur der CSS-Datei geändert würde 
                if line_without_comment != dictchanges[current_file]["newvalues"][icurrent_attr]:
                    bchange = True
                    
            if bchange:
                f.write(line.replace(line_without_comment,dictchanges[current_file]["newvalues"][icurrent_attr]))
            else:
                f.write(line)
            
    f.close()
#"""             
  
os.system("/usr/bin/canberra-gtk-play --id='system-ready'") #System-Sound abspielen, um Ende zu signalisieren
print("Ende")
