# Lõputöö - Henri Seppel Inimese emotsioonide tuvastamine kaamerapildi alusel

# Metoodika:
Programm loeb pildid kahest kaustast "real" ja "fake". Pildi pealt tuvastatakse vastavad elemendid: nägu, silm ja suu. Elemendid salvestatakse eraldi jpg failidena nende vastavatesse kaustadesse. Järgnevalt loetakse elemendid kaustadest ning ehitatatkse vastavad andmeraamistikud, andes elementide piltidele kaasa väärtused: nimi, tee (path) ning klass (1- real, 0 - fake). Ehitatakse valmis masinõppe mudel kasutades baasina VGG16 eeltreenitud kihte. Elementide andmeraamistike põhjal valmistatakse iteraatorid mille põhjal treenitakse 3 masinõppe mudelit - eraldi nägude, silmade ja suude jaoks.

Kaustast 'ennustused' loeb programm pildid ning jaotab need kolmeks elemendiks erlaid kaustadesse. Treenitud mudelite põhjal otsustatakse, kas ennustustes antud elemendid on 1- real või 0-fake. Luuakse lõplike tulemuste andmeraamistik kus kuvatakse ennustatava pildi lõplik tulemus.

Osad:

# Andmed.py - faili ülesanne on piltide leidmine, töötlemine, jaotamine kaustadesse ja andmestike tekitamine

Pilt jaotatakse kolmeks elemendiks ja salvestatakse oma kaustadesse. Pildid jaotatakse treenimise ja kontrollimise andmeraamistikeks.
![image](https://user-images.githubusercontent.com/58773522/205363251-ed57cf32-2f9f-4eab-8cac-94f7806f560c.png)

# Mudelid.py - faili ülesanne on masinõppe mudelite ehitamine, jooksutamine ja salvestamine

Andmeraamistike põhjal ehitab mudelid ning treenib neid vastavalt elemendile.
Näide: Nägude mudelit treenimine
![nägude_mudel_2](https://user-images.githubusercontent.com/58773522/205363697-fdcaf075-2964-4de8-ac70-1a8b3182f7f6.JPG)

Ülesobitamise vältimiseks kasutab andmete rikastamise (data augmentation) ja varajase lõpetamise meetodeid.
![pilt_augment_1](https://user-images.githubusercontent.com/58773522/205363905-1571f1cf-2106-4a30-91ad-af91cd8beb88.JPG)

# Tulemused.py - faili ülesanne on treentiud mudelite abil ennustada pilte ning klassifitseerida nad kas 1-real või 0-fake

Annab protsentides pildi tulemuse
![protsendid_1](https://user-images.githubusercontent.com/58773522/205364269-a5374376-7d33-4d58-9d29-dbc753337616.PNG)


Lõplike tulemuste kuvamine
![lõpp_1](https://user-images.githubusercontent.com/58773522/205364213-8c4e7235-6a7f-49ad-89d4-20666240513b.PNG)

Salvestab lõplikud tulemused csv faili



# Setup:
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
    
- ennustused
    - pildid
    - näod
    - silmad
    - suud
    
    
