from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from keras import optimizers
from keras.applications import VGG16
from keras.callbacks import EarlyStopping
from keras.layers import Dropout, Flatten, Dense, GlobalMaxPooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from xx_andmed import andmebaaside_tekitamine, piltide_töötlemine


# Faili ülesanne on masinõppe mudelite ehitamine, jooksutamine ja salvestamine

# Funktsioon võtab mudeli ehitamise andmed ja esitab need graafikul
def mudeli_graafik(ajalugu):
    # graafiku peal olevad näidud, võetud andmestikust
    acc = ajalugu.history['accuracy']
    val_acc = ajalugu.history['val_accuracy']
    loss = ajalugu.history['loss']
    val_loss = ajalugu.history['val_loss']
    length = range(len(acc))

    # graafikule joonistamine
    plt.plot(length, acc, label='Acc')
    plt.plot(length, val_acc, label='Val_Acc')
    plt.plot(length, loss, label='loss')
    plt.plot(length, val_loss, label='Val_loss')

    # graafiku esitamine
    plt.title('Tulemused')
    plt.legend()
    plt.show()


# Funktsioon ehitab mudeli kasutades eeltreentud mudelit ja lisab sinna kihte
def mudeli_ehitamine(suurus):
    kuju = (suurus, suurus, 3)  # pildi jada "kuju"

    # valmis treenitud baas mudel - VGG16
    baas_mudel = VGG16(
        input_shape=kuju,
        include_top=False,
        weights="imagenet"  # varasemalt kaalutletud imagenet andmebaasi klassifikatsiooni põhjal
    )

    # eeltreenitud mudeli viimasele kihile lisame juurde kihte
    viimane_kiht = baas_mudel.get_layer('block5_pool').output

    kihid = GlobalMaxPooling2D()(viimane_kiht)  # ruumiliste andmete keskmiste ühendamine
    kihid = Dense(512, activation='relu')(kihid)   # Neural Network kiht, Rectified Linear Unit aktiveerimine
    kihid = Flatten()(kihid)  # andmete lisatakse lisa dimensiooniline kiht nt: (10) -> (10, 1)
    kihid = Dropout(0.5)(kihid)  # aitab overfitting vastu
    kihid = Dense(1, activation='sigmoid')(kihid)

    mudel = Model(baas_mudel.input, kihid)  # liidab kihid mudelisse kokku
    # optimeerija tüüp Gradient Descent, õppimise kiirus 0.0001, momentum - parameeter mis liigub õppimise suunas
    mudel.compile(optimizer=optimizers.SGD(learning_rate=1e-4, momentum=0.9), loss='binary_crossentropy',
                  metrics=['accuracy'])  # loss - binary_crossentropy, klassifeerib 1/0 vahel, mõõdab täpsuse järgi
    mudel.summary()

    return mudel


# Funktsioon andmete generaatori ja iteraatori ehitamiseks
def generaatorite_ehitamine(trenn, kontroll, suurus, plokk):
    trenn_data = ImageDataGenerator(  # aitab overfitting vastu, algsete piltide andmete rikastamine (data augmentation)
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    trenn_gen = trenn_data.flow_from_dataframe(
        trenn,
        x_col='tee',
        y_col='klass',
        target_size=(suurus, suurus),
        class_mode='raw',
        batch_size=plokk
    )

    kont_data = ImageDataGenerator(rescale=1. / 255)
    kont_gen = kont_data.flow_from_dataframe(
        kontroll,
        x_col='tee',
        y_col='klass',
        target_size=(suurus, suurus),
        class_mode='raw',
        batch_size=plokk
    )

    return trenn_gen, kont_gen


# Funktsioon näitamaks kuidas generaator muudab pilte
def pildi_augmentatsiooni_kuvamine(andmestik):
    trenn_data = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # näidis andmebaas ja generaator mis võtab 1 suvalise pildi
    näidis_df = andmestik.sample(n=1).reset_index(drop=True)
    näidis_gen = trenn_data.flow_from_dataframe(
        dataframe=näidis_df,
        x_col='tee',
        y_col='klass',
        class_mode='raw'
    )

    # paneb pildid joonestiku peale
    plt.figure(figsize=(12, 12))
    for i in range(0, 9):
        plt.subplot(3, 3, i + 1)
        for x, y in näidis_gen:
            pilt = x[0]
            plt.imshow(pilt)
            break
    plt.tight_layout()
    plt.show()


# Funktsioon mis ehitab ja treenib mudelit
def mudeli_jooksutamine(mudel, epohh, trenn_gen, kont_gen, kannatus):
    varajane_stopp = EarlyStopping(monitor='val_accuracy', patience=kannatus)

    mudeli_tulemus = mudel.fit(
        trenn_gen,
        epochs=epohh,
        validation_data=kont_gen,
        # callbacks=[varajane_stopp]  # peatab mudeli treenimise enneaegselt kui arenemine lõppeb
    )

    return mudeli_tulemus


# Käsklus mis töötleb algseid piltide kaustasid, funktsioon tuleb failist andmed.py
piltide_töötlemine()

# MAIN
IMG_SIZE = 144
plokk = 16
epokk = 50
# tekitan andmestikud
# Andmebaasist poolitatud piltide arv protsentuaalsest, mida kasutatakse treenimisel
lahutatud_piltide_arv = 0.2  # 20% täis kogusest
# tekitame andmebaasid, igale elemendile oma treening- ja kontrollandmed
näod_trenn, näod_kont, suud_trenn, suud_kont, silm_trenn, silm_kont = andmebaaside_tekitamine(lahutatud_piltide_arv)

print("Näod andmestikud:", len(näod_trenn), len(näod_kont))
print("Suud andmestikud:", len(suud_trenn), len(suud_kont))
print("Silm andmestikud:", len(silm_trenn), len(silm_kont))

# NÄOD
mudel = mudeli_ehitamine(IMG_SIZE)  # mudel nägude jaoks
# generaatorid mudeli jooksutamise jaoks
nägude_treening_gen, nägude_kontroll_gen = generaatorite_ehitamine(näod_trenn, näod_kont, IMG_SIZE, plokk)
# treenime nägude mudelit
nägude_tulem = mudeli_jooksutamine(mudel, epokk, nägude_treening_gen, nägude_kontroll_gen, kannatus=5)
# tulemi graafiku peal esitamine
mudeli_graafik(nägude_tulem)
# mudeli salvestamine
mudel.save("mudel_näod_1")

pildi_augmentatsiooni_kuvamine(näod_trenn)

# SUUD
mudel = mudeli_ehitamine(IMG_SIZE)
suude_treening_gen, suude_kontroll_gen = generaatorite_ehitamine(suud_trenn, suud_kont, IMG_SIZE, plokk)
suude_tulem = mudeli_jooksutamine(mudel, epokk, suude_treening_gen, suude_kontroll_gen, kannatus=5)
# tulemi graafiku peal esitamine
mudeli_graafik(suude_tulem)
# mudeli salvestamine
mudel.save("mudel_suud_1")

# SILMAD
mudel = mudeli_ehitamine(IMG_SIZE)
# generaatorid mudeli jooksutamise jaoks
silmade_treening_gen, silmade_kontroll_gen = generaatorite_ehitamine(silm_trenn, silm_kont, IMG_SIZE, plokk)
silmade_tulem = mudeli_jooksutamine(mudel, epokk, silmade_treening_gen, silmade_kontroll_gen, kannatus=5)
# tulemi graafiku peal esitamine
mudeli_graafik(silmade_tulem)
# mudeli salvestamine
mudel.save("mudel_silmad_1")
