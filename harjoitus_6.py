import tkinter as tk
import random
import threading
import numpy as np
import time

# SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA (1 PISTETTÄ) ALKAA TÄSTÄ

# Luodaan pääikkuna
ikkuna = tk.Tk()
ikkuna.title("Turvallinen uima-allas")
ikkuna.geometry("1000x800+1300+100")
ikkuna.configure(bg='blue')  # Asetetaan taustaväri siniseksi (valtameri)

# Luodaan autiosaari
autiosaari = tk.Canvas(ikkuna, width=800, height=600, bg='#eab676', highlightthickness=0)  # Hiekkainen saari
autiosaari.place(anchor='center', relx=0.5, rely=0.5)

# Määritellään uima-allas (20x60), aluksi täynnä nollia (tyhjä)
uima_allas = [[0 for _ in range(60)] for _ in range(20)]

# Määritellään ojat (100x1), aluksi täynnä ykkösiä (hiekkaa)
oja_ernesti = [[1] for _ in range(100)]
oja_kernesti = [[1] for _ in range(100)]

# Määritellään metsäalue (20x60) numpytaulukkona, täynnä ykkösiä (metsä)
metsa = np.ones((20, 60), dtype=int)

# Funktio, joka piirtää uima-altaan
def piirra_uima_allas():
    ruudun_koko = 5  # Yhden ruudun koko 5x5 pikseliä
    for i in range(20): # luodaan taulukko 20x60
        for j in range(60):  
            x0, y0 = j * ruudun_koko, i * ruudun_koko # Ruudun vasemman yläkulman koordinaatit
            x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
            väri = "#eab676" if uima_allas[i][j] == 0 else "blue" # Hiekka = keltainen, vesi = sininen  
            autiosaari.create_rectangle(x0 + 250, y0 + 250, x1 + 250, y1 + 250, fill=väri, outline='grey') # Piirretään uima-allas

# Funktio, joka piirtää ojat ja ottaa parametreina ojan, aloituspisteen x- ja y-koordinaatit
def piirra_oja(oja, x_alku, y_alku):
    ruudun_koko = 2.5      # Yhden ruudun koko 5x5 pikseliä
    for i in range(100): # luodaan taulukko 100x1
        x0, y0 = x_alku, y_alku - i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
        x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit 
        if oja[i][0] == 0:      # Jos oja on kaivettu, väri on ruskea
            väri = "#8e6f4e"
        elif oja[i][0] == 2:    # Jos oja on täytetty vedellä, väri on sininen
            väri = "blue"
        else:                   # Muuten väri on keltainen
            väri="#eab676"
        autiosaari.create_rectangle(x0, y0, x1, y1, fill=väri, outline='grey') # Piirretään oja

# Funktio, joka piirtää metsäalueen
def piirra_metsa():
    ruudun_koko = 5  # Yhden ruudun koko 5x5 pikseliä
    for i in range(20):  # Piirretään vain tarvittavat ruudut
        for j in range(60):
            if metsa[i][j] == 1:  # Piirretään vain metsäruudut
                x0, y0 = j * ruudun_koko, i * ruudun_koko
                x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
                autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill="green", outline='green')

def paivita_metsa(i, j, arvo):
    metsa[i][j] = arvo
    ruudun_koko = 5
    x0, y0 = j * ruudun_koko, i * ruudun_koko
    x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
    väri = "green" if arvo == 1 else "brown"
    autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill=väri, outline='green')

# Piirretään aluksi uima-allas ja ojat (täynnä hiekkaa)
piirra_uima_allas()
piirra_oja(oja_ernesti, 250, 246)  # Ernestin oja
piirra_oja(oja_kernesti, 545, 246)  # Kernestin oja
piirra_metsa()  # Piirretään metsäalue

# SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA (1 PISTETTÄ) PÄÄTTYY TÄHÄN

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) ALKAA TÄSTÄ

# Funktio, jolla luodaan apinoita satunnaisiin paikkoihin metsään

apinoiden_tiedot = []   # Lista apinoiden tiedoista 

def luo_apina():
    for i in range(10):  # Lisätään 5 apinaa
        apina_x = random.randint(0, 59)  # Arvotaan apinan x-koordinaatti
        apina_y = random.randint(0, 19)  # Arvotaan apinan y-koordinaatti
        metsa[apina_y][apina_x] = 0      # Asetetaan apina metsään
        paivita_metsa(apina_y, apina_x, 0)  # Päivitetään metsä

def e_hakee_apinan():
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)
    while [y_koordinaatti_oja, y_koordinaatti] in apinoiden_tiedot:
        y_koordinaatti = random.randint(0, 249)
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)
        
    # Määritetään x-koordinaatti Ernestin ojan varrelle
    x_koordinaatti = 0

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:
                metsa[i][j] = 1
                x_koordinaatti = j
                paivita_metsa(i, j, 1)  
                autiosaari.create_oval(245, y_koordinaatti, 250, y_koordinaatti + 5, fill='brown', outline='brown') 
                apinoiden_tiedot.append([y_koordinaatti_oja, y_koordinaatti])  
                apinoiden_tiedot_sorted = sorted(apinoiden_tiedot, key=lambda x: x[0])
                print("Apinoiden tiedot järjestyksessä:", apinoiden_tiedot_sorted)
                break
            elif i == 19 and j == 59:
                print("Metsässä ei ole apinoita!")
                break
        if x_koordinaatti != 0:
            break
    
def e_apina_kaivaa_ojaa():
    global apinoiden_tiedot
    if len(apinoiden_tiedot) == 0:
        print("Ei apinoita kaivamassa!")
        return
    
    apina_sijainti = apinoiden_tiedot[0]  # Otetaan ensimmäinen apina listasta
    y_sijainti = apina_sijainti[0]  # Apinan sijainti ojan varrella
    x_sijainti = 0  # Alussa apina on ojan alussa

    kaivamis_nopeus = 1  # Kaivamisnopeus alkaa yhdestä sekunnista metriä kohti
    kaivettu_pituus = 0  # Alussa ei ole kaivettu metriäkään

    while kaivettu_pituus < 100:  # Kaivetaan kunnes oja on täyteen kaivettu
        if oja_ernesti[kaivettu_pituus][0] == 1:  # Jos ojaa ei ole vielä kaivettu tässä kohtaa
            oja_ernesti[kaivettu_pituus][0] = 0  # Kaiva kohta
            piirra_oja(oja_ernesti, 250, 246)  # Päivitetään oja
            print(f"Apina kaivoi kohdan: {kaivettu_pituus}")
            
            # Soitetaan kaivamisääniefekti (placeholder-ääni)
            print("Kaivamisääni!")  # Voit lisätä tähän oikean äänen käyttämällä esimerkiksi Pygamea

            time.sleep(kaivamis_nopeus)  # Apina kaivaa metrin ja pitää tauon
            kaivettu_pituus += 1  # Siirrytään seuraavaan kohtaan

            # Päivitetään apinan sijainti ojan varrella visuaalisesti
            autiosaari.create_oval(245, y_sijainti - kaivettu_pituus * 2.5, 250, y_sijainti - (kaivettu_pituus * 2.5) + 5, fill='brown', outline='brown')

            # Väsymys: Kaivaminen hidastuu kaksinkertaiseksi joka kerta
            kaivamis_nopeus *= 2
    

# Luodaan painike, jolla lisätään apinoita
lisaa_apinoita = tk.Button(ikkuna, text="Lisää apinoita", command=luo_apina)
lisaa_apinoita.place(x=100, y=100)

# Luodaan painike, jolla Ernesti hakee apinan
ernesti_hakee_apinan = tk.Button(ikkuna, text="Ernesti hakee apinan", command=lambda: threading.Thread(target=e_hakee_apinan).start()) # Kutsutaan funktiota ernesti_hakee_apinan, jokainen apinan haku käynnistyy omassa threadissaan
ernesti_hakee_apinan.place(x=100, y=150)

# Luodaan painike, jolla apina alkaa kaivamaan ojaa
e_apina_kaivaa_ojaa_btn = tk.Button(ikkuna, text="Apina kaivaa Ernestin ojaa", command=e_apina_kaivaa_ojaa)
e_apina_kaivaa_ojaa_btn.place(x=100, y=200)

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) PÄÄTTYY TÄHÄN

# Käynnistä ohjelma
ikkuna.mainloop()
