import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.models import load_model
from keras_preprocessing.image import ImageDataGenerator, load_img

from xx_andmed import ennustuste_töötlemine

piltide_kaust = ''


# Funktsioon salvestab andmesitku csv. failina excelisse
def salvestan_andmestiku_excelisse(andmestik, nimi):
    andmestik.to_csv(nimi + '.csv')


# Funktsioon leiab kaustas üles ennustuse pildid ja lisab need andmeraamistikku
def piltide_hankimine():
    tee = []
    nimi = []

    for pildid in os.listdir(piltide_kaust + 'pildid'):
        tee.append(piltide_kaust + 'pildid//' + pildid)
        nimi.append(pildid)

    andmestik = pd.DataFrame({
        'tee': tee,
        'nimi': nimi,
    })

    return andmestik


# Funktsioon hangib olemasolevatest jaotatud elementidega kaustadest pildid ja lisab andmeraamistikku
def piltide_elementide_hankimine(kaust):
    tee = []
    nimi = []

    for pildid in os.listdir(piltide_kaust + kaust):
        tee.append(piltide_kaust + kaust + '//' + pildid)
        nimi.append(pildid)

    andmestik = pd.DataFrame({
        'tee': tee,
        'nimi': nimi,
    })

    return andmestik


# Funktsioon andmete generaatori ja iteraatori ehitamiseks
def generaatori_ehitamine(andmed, pilt_suurus, plokk):
    generaator = ImageDataGenerator(rescale=1. / pilt_suurus)
    iteraator = generaator.flow_from_dataframe(
        andmed,
        x_col='tee',
        y_col='nimi',
        target_size=(pilt_suurus, pilt_suurus),
        class_mode='raw',
        batch_size=plokk
    )

    return iteraator


# Funktsioon võtab salvestatud mudeli ja jookseb läbi piltide iteraatori lisades andmestikku ennustuse tulemusi
def ennustan_pildid(mudel, andmestik, iteraator):
    # jooksutades läbi iteraatori, annab pildile tulemuse mudeli hinnangu põhjal
    ennustus = mudel.predict(iteraator)
    # lisame andemstikku pildi tulemuse, 1 ehk Real on kui tulemus üle 0.5, 0 ehk Fake kui alla
    andmestik['tulemus'] = np.where(ennustus > 0.5, 1, 0)
    # lisame andmestikku protsentuaalse tulemuse
    andmestik['protsent'] = ennustus
    # tagastan täiendatud andmestiku
    return andmestik


# Funktsioon ennustatud andmetiku kuvamiseks
def ennustuse_kuvamine(andmestik, suurus):
    # Võtab ennustatud andmestikust suvalised 9 pilti koos nende kaasa antud ennustatud väärtustega
    näited = andmestik.sample(n=9).reset_index()

    # Pildiraamistiku ehitamine ning piltide lisamine
    plt.figure(figsize=(12, 12))
    for i in range(0, len(näited)):
        pilt = load_img(näited['tee'][i], target_size=(suurus, suurus))
        nimi = näited['nimi'][i]
        klass = näited['tulemus'][i]
        protsent = näited['protsent'][i]
        plt.subplot(3, 3, i + 1)
        plt.imshow(pilt)
        plt.xticks([])  # eemaldab pildi küljelt telgjoone
        plt.yticks([])

        if klass == 1:  # Kui ennusttaud klass on 1 ehk REAL
            # toob pildi all välja tulemuse
            plt.xlabel(nimi + ' - REAL {}'.format(klass))
            # kirjutab välja protsentides pildi tulemuse
            print(nimi, " - pilt on {:.2f}% REAL ja {:.2f}% FAKE".format(protsent, (1 - protsent)))
        else:
            plt.xlabel(nimi + ' - FAKE {}'.format(klass))
            print(nimi, " - pilt on {:.2f}% REAL ja {:.2f}% FAKE".format(protsent, (1 - protsent)))

    plt.tight_layout()
    plt.show()


# Funktsioon võtab andmeraamistikust igale elemendile antud ennustuse väärtuse ning lisab lõpliku ennustuste tulemi
# Kuna lõplik ennustus koosneb 3 eraldi elemendi ennustusest, siis kui lõplike väärtuste summa on üle 2
# ehk vähemalt 66% siis on lõplik ennustus REAL, kui summa on alla 2 siis on lõplik ennustus FAKE
def lõplik_ennustus(andmestik, nägude_tulem, suude_tulem, silmade_tulem):

    for i in range(len(andmestik)):
        andmestik['nägu'] = nägude_tulem['tulemus'][i]
        andmestik['suu'] = suude_tulem['tulemus'][i]
        andmestik['silm'] = silmade_tulem['tulemus'][i]

        if (nägude_tulem['tulemus'][i] + suude_tulem['tulemus'][i] + silmade_tulem['tulemus'][i]) >= 2:
            # REAL
            andmestik['tulemus'] = 1
        else:
            # FAKE
            andmestik['tulemus'] = 0

    return andmestik


# MAIN
IMG_SUURUS = 144
plokk = 1

# andmete failist, lõikab ja liigutab pilte
ennustuste_töötlemine()


# algsete ennustuse piltide andmestik kuhu lisan lõplikud tulemused
piltide_andmestik = piltide_hankimine()

# Algsete piltide leidmine ja nende andmestikku panemine, siia kirjutan lõpliku tulemuse kokku
nägude_andmestik = piltide_elementide_hankimine("näod")
suude_andmestik = piltide_elementide_hankimine("suud")
silmade_andmestik = piltide_elementide_hankimine("silmad")

# Eraldi elementide iteraatoprite ehitamine
nägude_iteraator = generaatori_ehitamine(nägude_andmestik, IMG_SUURUS, plokk)
suude_iteraator = generaatori_ehitamine(suude_andmestik, IMG_SUURUS, plokk)
silmade_iteraator = generaatori_ehitamine(silmade_andmestik, IMG_SUURUS, plokk)

# laeme mudelid
nägud_mudel = load_model('mudel_näod_1', compile=True)
suude_mudel = load_model('mudel_suud_1', compile=True)
silmade_mudel = load_model('mudel_silmad_1', compile=True)

# Ennustan iga elemendi
nägude_tulem = ennustan_pildid(nägud_mudel, nägude_andmestik, nägude_iteraator)
suude_tulem = ennustan_pildid(suude_mudel, suude_andmestik, suude_iteraator)
silmade_tulem = ennustan_pildid(silmade_mudel, silmade_andmestik, silmade_iteraator)

# Lõplik andmeraamistik kõikide ennustustega ja lõpliku tulemusega
piltide_andmestik = lõplik_ennustus(piltide_andmestik, nägude_tulem, suude_tulem, silmade_tulem)


ennustuse_kuvamine(nägude_tulem, IMG_SUURUS)
ennustuse_kuvamine(suude_tulem, IMG_SUURUS)
ennustuse_kuvamine(silmade_tulem, IMG_SUURUS)

ennustuse_kuvamine(piltide_andmestik, IMG_SUURUS)

salvestan_andmestiku_excelisse(nägude_tulem, "näod_tulem")
salvestan_andmestiku_excelisse(suude_tulem, "suude_tulem")
salvestan_andmestiku_excelisse(silmade_tulem, "silmade_tulem")

