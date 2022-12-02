# Lõputöö - Henri Seppel Inimese emotsioonide tuvastamine kaamerapildi alusel

Metoodika:
Programm loeb pildid kahest kaustast "real" ja "fake". Pildi pealt tuvastatakse vastavad elemendid: nägu, silm ja suu. Elemendid salvestatakse eraldi jpg failidena nende vastavatesse kaustadesse. Järgnevalt loetakse elemendid kaustadest ning ehitatatkse vastavad andmeraamistikud, andes elementide piltidele kaasa väärtused: nimi, tee (path) ning klass (1- real, 0 - fake). Ehitatakse valmis masinõppe mudel kasutades baasina VGG16 eeltreenitud kihte. Elementide andmeraamistike põhjal valmistatakse iteraatorid mille põhjal treenitakse 3 masinõppe mudelit - eraldi nägude, silmade ja suude jaoks.

Kaustast 'ennustused' loeb programm pildid ning jaotab need kolmeks elemendiks erlaid kaustadesse. Treenitud mudelite põhjal otsustatakse, kas ennustustes antud elemendid on 1- real või 0-fake. Luuakse lõplike tulemuste andmeraamistik kus kuvatakse ennustatava pildi lõplik tulemus.

Osad:

Andmed.py - faili ülesanne on piltide leidmine, töötlemine, jaotamine kaustadesse ja andmestike tekitamine
![f1](https://user-images.githubusercontent.com/58773522/205362922-d93997b7-c006-45c8-b2f4-7ad419323167.JPG)



Setup:
Python install vajalikud paketid: Pillow, Keras, SKLearn, Pandas, Numpy, OpenCV, MatPlotLib

KAUSTADE HIERARHIA
Alustame kahe kaustaga kus on päris ja võlts pildid oma kaustades

- pildid
    - pildid_fake
    - pildid_real
    - näod
        - fake näod
        - real näod
    - silmad
        - fake silmad
        - real silmad
    - suud
        - fake suud
        - real suud
    - pakkumised
    
- ennustused
    - pildid
    - näod
    - silmad
    - suud
    
    
