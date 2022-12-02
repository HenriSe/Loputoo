import os
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from keras.utils import load_img
from sklearn.model_selection import train_test_split

"""
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
"""

# Faili ülesanne on piltide leidmine, töötlemine, jaotamine kaustadesse ja andmestike tekitamine

# HaarCascade näo elementide failid OpenCV masinnägemise teegist
silma_cascade = cv2.CascadeClassifier("venv\Lib\site-packages\cv2\data\haarcascade_eye.xml")
suu_cascade = cv2.CascadeClassifier("venv\Lib\site-packages\cv2\data\haarcascade_smile.xml")
näo_cascade = cv2.CascadeClassifier("venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml")
piltide_kaust = ' '
ennustuste_kaust = ' '

IMG_SIZE = 144  # üleüldine pildi suurus läbivalt läbi terve koodi

# Funktsioon leiab üles näo pildi pealt elemendi (nägu, suu, silm) ning eraldab selle
def näo_töötlemine(element, pilt, scalar):

    pilt = load_img(pilt, target_size=(IMG_SIZE, IMG_SIZE))
    pilt = pilt.convert('L')  # muudan pildid grayscaleks
    pilt = np.array(pilt, dtype='uint8')

    # vastavalt tingimusele otsin eraldi elementi
    if element == 'nägu':
        otsija = näo_cascade.detectMultiScale(pilt, scalar, 5)
    if element == 'suu':
        otsija = suu_cascade.detectMultiScale(pilt, scalar, 20)
    if element == 'silm':
        otsija = silma_cascade.detectMultiScale(pilt, scalar, 5)

    # joonistab ümber otsitava elemendi ristküliku ja lõikab selle välja
    for (x, y, w, h) in otsija:
        cv2.rectangle(pilt, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        otsija = pilt[y:y + h, x:x + w]
        otsija = cv2.resize(otsija, (IMG_SIZE, IMG_SIZE))

    otsija = Image.fromarray(otsija)
    return otsija

# Funktsioon jookseb läbi kõikide kaustades olevate piltide
# ja leiab nendele vastavad elemendid mis salvestatakse eraldi kaustadesse
def piltide_töötlemine():
    for kaustad in os.listdir(piltide_kaust):
        if kaustad == 'pildid_real':  # klassifitseeritud reaalse naeratusega pildid
            for pildid in os.listdir(piltide_kaust + 'pildid_real'):
                print(kaustad, pildid)

                pilt = piltide_kaust + 'pildid_real//' + pildid

                nägu = näo_töötlemine('nägu', pilt, 1.1)
                nägu.save('C://Henri//Desktop//loputoo//pildid//näod//real_näod//' + pildid)

                suu = näo_töötlemine('suu', pilt, 1.1)
                suu.save('C://Henri//Desktop//loputoo//pildid//suu//real_suu//' + pildid)

                silm = näo_töötlemine('silm', pilt, 1.05)
                silm.save('C://Henri//Desktop//loputoo//pildid//silmad//real_silmad//' + pildid)

        if kaustad == 'pildid_fake':  # klassifitseeritud võltsi naeratusega pildid
            for pildid in os.listdir(piltide_kaust + 'pildid_fake'):
                print(kaustad, pildid)

                pilt = piltide_kaust + 'pildid_fake//' + pildid

                nägu = näo_töötlemine('nägu', pilt, 1.1)
                nägu.save('C://Henri//Desktop//loputoo//pildid//näod//fake_näod//' + pildid)

                suu = näo_töötlemine('suu', pilt, 1.1)
                suu.save('C://Henri//Desktop//loputoo//pildid//suu//fake_suu//' + pildid)

                silm = näo_töötlemine('silm', pilt, 1.05)
                silm.save('C://Henri//Desktop//loputoo//pildid//silmad//fake_silmad//' + pildid)


# Funktsioon teeb sama mis ülemine, aga seekord jookseb läbi ennustuseks ette antud piltide elemendid
def ennustuste_töötlemine():
    for kaustad in os.listdir(ennustuste_kaust):
        if kaustad == 'pildid':
            for pildid in os.listdir(ennustuste_kaust + 'pildid'):
                print(pildid)
                pilt = ennustuste_kaust + 'pildid//' + pildid

                nägu = näo_töötlemine('nägu', pilt, 1.1)
                nägu.save('C://Henri//Desktop//loputoo//ennustused//näod//' + pildid)

                suu = näo_töötlemine('suu', pilt, 1.1)
                suu.save('C://Henri//Desktop//loputoo//ennustused//suud//' + pildid)

                silm = näo_töötlemine('silm', pilt, 1.05)
                silm.save('C://Henri//Desktop//loputoo//ennustused//silmad//' + pildid)

# Funktsioon jookseb läbi kõikide piltide ja elementide mis asetsevad omad kasuatdes ning
# tekitab vastavad andmebaasid, lisades piltidele juurde asukoha, nime ja klassi väärtuse
def andmebaaside_tekitamine(testimise_suurus):
    # 6 erinevat kausta ja 3 erinevat andmebaasi
    nägu_nimi, nägu_tee, nägu_klass = [], [], []
    suu_nimi, suu_tee, suu_klass = [], [], []
    silm_nimi, silm_tee, silm_klass = [], [], []

    # jooksutab läbi nägu kastis olevad 'real' ja 'fake' kaustad
    # tekitab andmebaasi pildi nime, klassi ja asukoha väärtustega
    for näo_kaustad in os.listdir(piltide_kaust + 'näod'):
        if näo_kaustad == 'fake_näod':
            for pildid in os.listdir(piltide_kaust + 'näod//fake_näod'):
                nägu_nimi.append(pildid)
                nägu_klass.append(0)  # 0 for fake
                nägu_tee.append(piltide_kaust + 'näod//fake_näod//' + pildid)
        if näo_kaustad == 'real_näod':
            for pildid in os.listdir(piltide_kaust + 'näod//real_näod'):
                nägu_nimi.append(pildid)
                nägu_klass.append(1)  # 1 for real
                nägu_tee.append(piltide_kaust + 'näod//real_näod//' + pildid)

    for suu_kaustad in os.listdir(piltide_kaust + 'suu'):
        if suu_kaustad == 'fake_suu':
            for pildid in os.listdir(piltide_kaust + 'suu//fake_suu'):
                suu_nimi.append(pildid)
                suu_klass.append(0)  # 0 for fake
                suu_tee.append(piltide_kaust + 'suu//fake_suu//' + pildid)
        if suu_kaustad == 'real_suu':
            for pildid in os.listdir(piltide_kaust + 'suu//real_suu'):
                suu_nimi.append(pildid)
                suu_klass.append(1)  # 1 for real
                suu_tee.append(piltide_kaust + 'suu//real_suu//' + pildid)

    for silma_kaustad in os.listdir(piltide_kaust + 'silmad'):
        if silma_kaustad == 'fake_silmad':
            for pildid in os.listdir(piltide_kaust + 'silmad//fake_silmad'):
                silm_nimi.append(pildid)
                silm_klass.append(0)  # 0 for fake
                silm_tee.append(piltide_kaust + 'silmad//fake_silmad//' + pildid)
        if silma_kaustad == 'real_silmad':
            for pildid in os.listdir(piltide_kaust + 'silmad//real_silmad'):
                silm_nimi.append(pildid)
                silm_klass.append(1)  # 1 for real
                silm_tee.append(piltide_kaust + 'silmad//real_silmad//' + pildid)

    # vastavate elementidega tekitatud andmebaasid
    näod = pd.DataFrame({
        'klass': nägu_klass,
        'tee': nägu_tee,
        'nimi': nägu_nimi
    })
    suud = pd.DataFrame({
        'klass': suu_klass,
        'tee': suu_tee,
        'nimi': suu_nimi
    })
    silmad = pd.DataFrame({
        'klass': silm_klass,
        'tee': silm_tee,
        'nimi': silm_nimi
    })

    # andmebaaside shufle ehk segamine
    näod = näod.sample(frac=1)
    suud = suud.sample(frac=1)
    silmad = silmad.sample(frac=1)

    # võtame igast andmebaasist protsentuaalse koguse ning
    näod_trenn, näod_kont = train_test_split(näod, test_size=testimise_suurus)
    suud_trenn, suud_kont = train_test_split(suud, test_size=testimise_suurus)
    silm_trenn, silm_kont = train_test_split(silmad, test_size=testimise_suurus)

    return näod_trenn, näod_kont, suud_trenn, suud_kont, silm_trenn, silm_kont
