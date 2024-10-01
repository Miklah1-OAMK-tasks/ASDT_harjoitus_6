import tkinter as tk
import random
import threading

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

# Määritellään metsäalue (20x20), täynnä ykkösiä (metsä)
metsa = [[1 for _ in range(60)] for _ in range(20)]

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
    for i in range(20): # luodaan taulukko 20x60
        for j in range(60):
            x0, y0 = j * ruudun_koko, i * ruudun_koko # Ruudun vasemman yläkulman koordinaatit
            x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
            väri = "green" if metsa[i][j] == 1 else "brown"  # Metsä = vihreä, muu hiekka = keltainen
            autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill=väri, outline='green') # Piirretään metsä

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
    for i in range(5):  # Lisätään 5 apinaa
        apina_x = random.randint(0, 59)  # Arvotaan apinan x-koordinaatti
        apina_y = random.randint(0, 19)  # Arvotaan apinan y-koordinaatti
        metsa[apina_y][apina_x] = 0      # Asetetaan apina metsään
        piirra_metsa()                   # Päivitetään metsän piirros

def e_hakee_apinan():
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)
    
    while [y_koordinaatti] in apinoiden_tiedot:
        y_koordinaatti = random.randint(0, 249)
    
    # Määritetään x-koordinaatti Ernestin ojan varrelle
    x_koordinaatti = 0

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:
                metsa[i][j] = 1
                x_koordinaatti = j
                autiosaari.create_oval(245, y_koordinaatti, 250, y_koordinaatti + 5, fill='brown', outline='brown') 
                apinoiden_tiedot.append([y_koordinaatti])  
                break
        if x_koordinaatti != 0:
            break
    
    apinoiden_tiedot_sorted = sorted(apinoiden_tiedot, key=lambda x: x[0])
    print("Apinoiden tiedot järjestyksessä:", apinoiden_tiedot_sorted)
    piirra_metsa()  # Päivitetään metsän piirros

def e_apina_kaivaa_ojaa():
    global apinoiden_tiedot
    for i in range(100):
        oja_ernesti[i][0] = 0
        piirra_oja(oja_ernesti, 250, 246)  # Ernestin oja
    

# Luodaan painike, jolla lisätään apinoita
lisaa_apinoita = tk.Button(ikkuna, text="Lisää apinoita", command=luo_apina)
lisaa_apinoita.place(x=100, y=100)

# Luodaan painike, jolla Ernesti hakee apinan
ernesti_hakee_apinan = tk.Button(ikkuna, text="Ernesti hakee apinan", command=lambda: threading.Thread(target=e_hakee_apinan).start()) # Kutsutaan funktiota ernesti_hakee_apinan, jokainen apinan haku käynnistyy omassa threadissaan
ernesti_hakee_apinan.place(x=100, y=150)

# Luodaan painike, jolla apina alkaa kaivamaan ojaa
e_apina_kaivaa_ojaa = tk.Button(ikkuna, text="Apina kaivaa Ernestin ojaa", command=e_apina_kaivaa_ojaa)
e_apina_kaivaa_ojaa.place(x=100, y=200)

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) PÄÄTTYY TÄHÄN

# Käynnistä ohjelma
ikkuna.mainloop()
