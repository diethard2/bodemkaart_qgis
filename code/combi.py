"""
lees 3 bestanden in: orde.csv, groep.csv en bodemomschrijving.
Maak 1 nieuw bestand aan die de gegevens van de 3 bestanden combineert.
"""

DIVERSEN = """|a GROEVE~Zand-, leem- of grindgroeve~|a GR~~
|b AFGRAV~Afgegraven~A|b AF~~
|c OPHOOG~Opgehoogd of opgespoten~|c OP~~
|d EGAL~Geegaliseerd~|d EG~~
|e VERWERK~Vergraven~|e VE~~
|f TERP~Oude bewoningsplaatsen~|f TE~~
|g MOERAS~Moeras~|g MO~~
|g WATER~Water~|g WA~~
|h BEBOUW~Bebouwing~|h BE~~
|h DIJK~Dijk~|h DIJ~~
|i BOVLAND~Bovenlandstrook~|i BO~~
|j MYNSTRT~Mijnstort~|j MY~~"""

def _combi_orde_groep(orde_stream, groep_stream):
    ## retourneert een lijst met gecombineerde inhoud van orde_stream
    ## groep_stream
    combilijst = []
    orde_list = {}
    i=0
    for regel in orde_stream:
        i+=1
        if i==1:
            continue
        regel = regel.strip()
        elementen = regel.split(",")
        orde_list[elementen[0]]=elementen[1]
    i=0
    for regel in groep_stream:
        regel = regel.strip()
        elementen = regel.split(";")
        i+=1
        if i==1:
            elementen[-1] = 'orde'
        else:
            id_orde = elementen[-1]
            if id_orde <> '':
                elementen[-1] = orde_list[id_orde]
        combilijst.append(elementen)
    return combilijst

def combi_orde_groep(ordebestand, groepbestand):
    ## retourneert een lijst met gecombineerde inhoud van ordebestand
    ## groepsbestand
    orde_stream = open(ordebestand)
    groep_stream = open(groepbestand)
    combi = _combi_orde_groep(orde_stream, groep_stream)
    orde_stream.close()
    groep_stream.close()
    return combi

def _create_groepen_keyed(groepen):
    groepen_keyed = {}
    for i, groep in enumerate(groepen):
        code = groep[0]
        groep_orde = groep[1:]
        groepen_keyed[code]=groep_orde
    return groepen_keyed

def _proces_regel(regel_omschrijving):
    classify_elements = {}
    print regel_omschrijving
    woorden = regel_omschrijving.split()
    classify_elements["code"]= woorden[0]
    classify_elements["groepcode"] = woorden[1]
    textuurcode = None
    kalkcode = None
    omschrijving = None
    iets = woorden[2]

    if iets.isdigit():
        textuurcode = iets
    elif iets is 'A':
        kalkcode = iets
    elif len(iets) is 1:
        #bijvoorbeeld letter b,s,c,r,d,k,z,p
        omschrijving = ' '.join(woorden[3:])
    else:
        omschrijving = ' '.join(woorden[2:])

    if textuurcode is not None:
        """derde element was textuurcode, dan is er misschien
        het vierde element een kalkcode"""
        iets = woorden[3]
        if iets in ('A','C'):
            kalkcode = iets
            omschrijving = ' '.join(woorden[4:])
        else:
            omschrijving = ' '.join(woorden[3:])

    classify_elements["textuurcode"] = textuurcode
    classify_elements["kalkcode"] = kalkcode
    classify_elements["omschrijving"] = omschrijving
        
    return classify_elements
    
    
def _classify(omschrijving_stream, groepen, classify_stream):
    groepen_keyed = _create_groepen_keyed(groepen)
    for regel_omschrijving in omschrijving_stream:
        regel_omschrijving = regel_omschrijving.strip()
        classify_elements = _proces_regel(regel_omschrijving)
        code = classify_elements["code"]
        omschrijving  = classify_elements["omschrijving"]
        groepcode = classify_elements["groepcode"]
        kalkcode = classify_elements["kalkcode"]
        textuurcode = classify_elements["textuurcode"]
        groep = ['','']
        if groepcode in groepen_keyed:
            groep = groepen_keyed[groepcode]
        elif kalkcode is 'A':
            groepcode = groepcode + ' A'
            if groepcode in groepen_keyed:
                groep = groepen_keyed[groepcode]
        record = (code, omschrijving, groepcode, groep[0], groep[1])
        classify_stream.write("~".join(record))
        classify_stream.write("\n")

def classify(ordebestand, groepbestand, bodemomschrijving, classify_bestand):
    classify_stream = open(classify_bestand,'w')
    groepen = combi_orde_groep(ordebestand, groepbestand)
    omschrijving_stream = open(bodemomschrijving)
    kopregel = ['code','omschrijving','groepcode','groep','orde']
    classify_stream.write("~".join(kopregel))
    classify_stream.write("\n")
    _classify(omschrijving_stream, groepen, classify_stream)
    classify_stream.write(DIVERSEN)
    omschrijving_stream.close()
    classify_stream.close()
    
def main():
    folder = r'C:\Users\diethard\Documents\qgis\projecten\bodemkaart'
    import os
    f_orde =  os.path.join(folder, 'orde.csv')
    f_groep = os.path.join(folder, 'groep.csv')
    f_omschrijving = os.path.join(folder, 'bodemomschrijving.txt')
    f_classify = os.path.join(folder, 'bodem.csv')
    classify(f_orde, f_groep, f_omschrijving, f_classify)

if __name__ == "__main__":
    main()
